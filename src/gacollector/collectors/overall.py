import codecs
import csv
import datetime
import os

from gacollector.collectors.column_picker import ColumnPicker
from gacollector.misc.comparer import file_get_date
from gacollector.settings.constants import ADDITIONAL_HEADERS, CSV_NULL_VALUES
from gacollector.settings.constants import DATE_OUT_FORMAT
from gacollector.settings.constants import ENC_IN, ENC_OUT


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
            # if self.headers != csv_rows.fieldnames:
            #     print(filename)
            #     print(self.headers)
            #     print(csv_rows.fieldnames)
            #     print()
            #     continue
            checked = False
            is_right = True
            for row in csv_rows:
                if not checked:
                    # for col_name in row.keys():
                    #     # if col_name not in self.headers:
                    #     #     print(filename)
                    #     #     print(row.keys())
                    #     #     print()
                    #     #     is_right = False
                    # if not is_right:
                    #     break
                    checked = True
                row = self._set_additional_headers_(row, additional_headers)
                for col in row.keys():
                    row[col] = row[col].encode(ENC_OUT, 'ignore').decode(ENC_OUT)
                    for char in CSV_NULL_VALUES:
                        row[col] = row[col].replace(char, '')
                # try:
                try:
                    writer.writerow(self._get_req_cols_(row))
                # except KeyError:
                #     # 7 0 1 3 5
                #     print(filename)
                #     print(row)
                #     print(self._get_req_cols_(row))
                except UnicodeEncodeError:
                    print(filename)
                    continue
                # except

    # 7 6 0 2 4

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
