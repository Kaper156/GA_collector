import codecs
import csv
import datetime
import decimal
import os
from decimal import Decimal, DecimalException

from check_csv_and_url import file_get_date
from column_picker import ColumnPicker
from constant_values import ADDITIONAL_HEADERS, CSV_NULL_VALUES
from constant_values import DATE_OUT_FORMAT
from constant_values import ENC_IN, ENC_OUT


class CsvCollector:
    def __init__(self, folder_with_csv, out_file_path):
        self.src_folder = folder_with_csv
        self.out_file_path = out_file_path
        self.additional_headers = ADDITIONAL_HEADERS
        self.headers = None
        self.column_picker = None

    def _handle_csv_files_rows_(self, writer):
        for filename, csv_rows in self._get_csv_readers_():
            additional_headers = self._get_additional_headers_for_file_(filename)
            for row in csv_rows:
                row = self._set_additional_headers_(row, additional_headers)
                writer.writerow(self._get_req_cols_(row))

    def _get_req_cols_(self, row):
        return self.column_picker.pick_row_cols(row)

    def write_out_csv(self):
        with open(self.out_file_path, 'w', newline='', encoding=ENC_OUT) as out_f:
            out_writer = csv.DictWriter(out_f, self._get_headers_())
            out_writer.writeheader()
            self._handle_csv_files_rows_(writer=out_writer)

    def _get_additional_headers_for_file_(self, filename):
        # Warning rewrite it if additional headers changed
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

                # Now it's None always, but in the future it can be configured from settings
                if self.column_picker is None:
                    self.column_picker = ColumnPicker(headers)
                self.headers = self.column_picker.pick_headers()
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

    @staticmethod
    def increment_row_by_row(row, row_def):
        for col_name, col_val in row.items():
            if col_name not in row_def.keys():
                continue  # If this col not specified
            _type = type(row_def[col_name])
            if _type in (str, None):
                continue
            if col_val in CSV_NULL_VALUES:
                col_val = '0'
            if _type is Decimal:
                col_val = RowTypeAggregator.str_to_decimal(col_val)
                col_val = col_val.replace('<$0.01', '0.01')
            try:
                col_val = _type(col_val)
            except ValueError:
                print(f'Error value={col_val} in file : ', row_def)
                col_val = 0
            except decimal.InvalidOperation:
                print(f'Error value={col_val} in file : ', row_def)
                col_val = 0
            row_def[col_name] += col_val
        return row_def


class CsvSummarize(CsvCollector):
    def __init__(self, folder_with_csv, out_file_path):
        super(CsvSummarize, self).__init__(folder_with_csv, out_file_path)
        self.row_defaults = None

    def _get_default_row_(self):
        # Should return copy of default row (ordered dict with headers with start values)
        if self.row_defaults:
            return self.row_defaults.copy()
        parse = RowTypeAggregator.get_row_default_values  # To convenience

        # Send csv files to parser, while them don't return def values
        for _, csv_rows in super()._get_csv_readers_():
            # Parsed bad file will return None
            while self.row_defaults is None:
                self.row_defaults = parse(next(csv_rows))

            # If we got row_def before next file
            if self.row_defaults is not None:
                # Return copy
                return self.row_defaults.copy()
        raise Exception("File do not contains rows, or all rows include blank values")

    def _handle_csv_files_rows_(self, writer):
        for filename, csv_rows in self._get_csv_readers_():

            file_row = self._get_default_row_()

            # Add additional headers before pick specified
            additional_headers = self._get_additional_headers_for_file_(filename)
            file_row = self._set_additional_headers_(file_row, additional_headers)

            # Pick only specified cols
            file_row = self.column_picker.pick_row_cols(file_row)

            for row in csv_rows:
                # row = self._get_req_cols_(row)
                file_row = RowTypeAggregator.increment_row_by_row(row, file_row)
            writer.writerow(file_row)


if __name__ == '__main__':
    CsvCollector('C:/Users/User/Documents/Programming/Python/Nika_GA/testing/sources/csv_by_week',
                 'test_inc.csv').write_out_csv()
    CsvSummarize('C:/Users/User/Documents/Programming/Python/Nika_GA/testing/sources/csv_by_week',
                 'test_sum.csv').write_out_csv()
