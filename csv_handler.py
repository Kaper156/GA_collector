import codecs
import csv
import datetime
import os
from decimal import Decimal, DecimalException

from check_csv_and_url import file_get_date
from constant_values import ADDITIONAL_HEADERS
from constant_values import DATE_OUT_FORMAT
from constant_values import ENC_IN, ENC_OUT


class CsvMerger:
    def __init__(self, folder_with_csv, out_file_path):
        self.src_folder = folder_with_csv
        self.out_file_path = out_file_path
        self.additional_headers = ADDITIONAL_HEADERS
        self.headers = None

    def _handle_csv_files_rows_(self, writer):
        for filename, csv_rows in self._get_csv_readers_():
            additional_headers = self._get_additional_headers_for_file_(filename)
            for row in csv_rows:
                row = self._set_additional_headers_(row, additional_headers)
                writer.writerow(row)

    def write_out_csv(self):
        with open(self.out_file_path, 'w', newline='', encoding=ENC_OUT) as out_f:
            out_writer = csv.DictWriter(out_f, self._get_headers_())
            out_writer.writeheader()
            self._handle_csv_files_rows_(writer=out_writer)

    def _get_additional_headers_for_file_(self, filename):
        d1, d2 = file_get_date(filename)
        d1, d2 = [datetime.datetime.strptime(d, "%Y%m%d") for d in (d1, d2)]
        week = d2.strftime("%V")
        is_week = f'{d1.year}{week}'
        if week == '01':  # If date_from is in previous year, but week started as first week in next year
            is_week = f'{d2.year}{week}'
        return {
            "From": d1.strftime(DATE_OUT_FORMAT),
            "To": d2.strftime(DATE_OUT_FORMAT),
            "Week": is_week
        }

    def _set_additional_headers_(self, row, header_values):
        row.update(header_values)
        return row

    def _get_headers_(self):
        if self.headers is not None:
            return self.headers
        for filename, csv_rows in self._get_csv_readers_():
            headers = csv_rows.fieldnames

            # Check for empty headers or something erorrs like that
            if type(headers) is list and type(headers[0]) is str:
                headers += self.additional_headers
                self.headers = headers
                break
        return self.headers

    def _get_csv_readers_(self):
        for filename, file_path in self._get_csv_filenames_and_paths_():
            with codecs.open(file_path, encoding=ENC_IN) as file:
                csv_rows = csv.DictReader(self._line_gen_file_(file), dialect="ga")

                yield filename, csv_rows

    def _line_gen_file_(self, file):
        start_is_skipped = False  # is established after skip head comments and empty line
        for line in file:
            if not start_is_skipped:  # Skip head useless info
                if line[:1] == '#':  # Skip comments block
                    continue
                if not line.strip():  # Skip empty line(s) after comments block
                    continue
            elif not line.strip():  # Stop before bottom avg, sum and others rows
                break
            yield line
            start_is_skipped = True  # At this point head info is skipped, next empty line is exact before avg-sum rows

    def _get_csv_filenames_and_paths_(self):
        for file_name in os.listdir(self.src_folder):
            file_path = os.path.join(self.src_folder, file_name)
            yield file_name, file_path


class RowTypeAggregator:
    @staticmethod
    def try_parse_default_values(row: csv.OrderedDict):
        if (None in row.values()) | ('-' in row.values()):
            return None
        for col in row.keys():
            val = row[col]
            if '$' in val:
                try:
                    Decimal(RowTypeAggregator.str_to_decimal(val))
                    yield col, Decimal()
                    continue
                except DecimalException:
                    pass
            try:
                int(val)
                yield col, int(0)
                continue
            except ValueError:
                pass
            try:
                float(val)
                yield col, float(0.0)
                continue
            except ValueError:
                yield col, str('-')

    @staticmethod
    def get_row_default_values(row: csv.OrderedDict):
        return csv.OrderedDict(RowTypeAggregator.try_parse_default_values(row))

    @staticmethod
    def str_to_decimal(val):
        return val.replace('$', '').replace(',', '').replace(' ', '')


class CsvAvg(CsvMerger):
    def __init__(self, folder_with_csv, out_file_path, operation='sum'):
        super(CsvAvg, self).__init__(folder_with_csv, out_file_path)
        self.additional_headers += ['File Name']
        self.row_defaults = None
        self.operation = operation.upper()  # TODO refactoring this

    def _get_row_defaults_(self):
        if self.row_defaults:
            return self.row_defaults.copy()
        parse = RowTypeAggregator.get_row_default_values

        for _, csv_rows in super()._get_csv_readers_():
            while self.row_defaults is None:
                self.row_defaults = parse(next(csv_rows))
            if self.row_defaults is not None:
                return self.row_defaults.copy()
        raise Exception("File do not contains rows, or all rows include blank values")

    # TODO refactoring this
    def _handle_csv_files_rows_(self, writer):
        for filename, csv_rows in self._get_csv_readers_():
            file_row = self._get_row_defaults_()
            for row in csv_rows:
                for col_name, col_val in row.items():
                    _type = type(file_row[col_name])
                    if _type in (str, None):
                        continue
                    if _type is Decimal:
                        col_val = RowTypeAggregator.str_to_decimal(col_val)

                        file_row[col_name] += _type(col_val)
            # If average, then each not str column should be divided to number of rows
            if self.operation == 'AVG':
                for col_name in file_row.keys():
                    if type(file_row[col_name]) is not str:
                        file_row[col_name] = file_row[col_name] / csv_rows.line_num

            # Set additional headers after, because they interfere calculations
            additional_headers = self._get_additional_headers_for_file_(filename)
            super()._set_additional_headers_(file_row, additional_headers)
            writer.writerow(file_row)


if __name__ == '__main__':
    CsvMerger('C:/Users/User/Documents/Programming/Python/Nika_GA/testing/sources/csv_by_week',
              'test_inc.csv').write_out_csv()
    CsvAvg('C:/Users/User/Documents/Programming/Python/Nika_GA/testing/sources/csv_by_week', 'test_avg.csv',
           'avg').write_out_csv()
    CsvAvg('C:/Users/User/Documents/Programming/Python/Nika_GA/testing/sources/csv_by_week', 'test_sum.csv',
           'sum').write_out_csv()
