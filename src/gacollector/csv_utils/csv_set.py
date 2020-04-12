import codecs
import csv

from gacollector.csv_utils.column_picker import ColumnPicker
from gacollector.misc.get_csv_from_folder import gen_csv_files_from_folder
from gacollector.settings.constants import ENC_IN, ENC_OUT


class CsvSet:
    def __init__(self, folder_with_csv, out_file_path, picked_columns_str):
        self.src_folder = folder_with_csv
        self.out_file_path = out_file_path
        self.headers = None

        self.column_picker = None
        self.picked_columns_str = picked_columns_str

        self.csv_writer = None
        self.csv_out_file = None

    def get_csv_writer(self):
        if self.csv_writer is None:
            self.csv_out_file = open(self.out_file_path, 'w', newline='', encoding=ENC_OUT)
            self.csv_writer = csv.DictWriter(self.csv_out_file, self._get_headers_())
            self.csv_writer.writeheader()
        return self.csv_writer

    def _get_headers_(self):
        if self.headers is not None:
            return self.headers
        for filename, csv_rows in self.get_csv_readers():
            headers = csv_rows.fieldnames

            # Check for empty headers or something errors like that
            if type(headers) is list and type(headers[0]) is str:
                headers = self.header_callback(headers)  # Callback for set-defaults
                headers += ("From", "To", "Week")
                self.column_picker = ColumnPicker(headers, self.picked_columns_str)
                self.headers = self.column_picker.pick_headers()
                break
        return self.headers

    # Be used in set-default types of summarize
    def header_callback(self, headers):
        return headers

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

    def get_csv_readers(self):
        for filename, file_path in gen_csv_files_from_folder(self.src_folder):
            with codecs.open(file_path, encoding=ENC_IN) as file:
                csv_rows = csv.DictReader(self._line_gen_file_(file), dialect="ga")
                yield filename, csv_rows

    def pick_only_choiced_cols(self, row):
        if self.headers is None:
            self._get_headers_()
        return self.column_picker.pick_row_cols(row)

    def write_out(self, row):
        self.get_csv_writer().writerow(row)

    def close(self):
        self.csv_out_file.close()
        self.csv_writer = None
