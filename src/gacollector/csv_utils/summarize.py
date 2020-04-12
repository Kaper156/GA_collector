from gacollector.csv_utils.overall import CsvCollector
from gacollector.csv_utils.row_type_aggregator import RowTypeAggregator


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
        for _, csv_rows in super().get_csv_readers():
            # Parsed bad file will return None
            while self.row_defaults is None:
                self.row_defaults = parse(next(csv_rows))

            # If we got row_def before next file
            if self.row_defaults is not None:
                # Return copy
                return self.row_defaults.copy()
        raise Exception("File do not contains rows, or all rows include blank values")

    def _handle_csv_files_rows_(self, writer):
        for filename, csv_rows in self.get_csv_readers():

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
