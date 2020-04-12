from gacollector.csv_utils.additional_headers import get_additional_fields_for_file
from gacollector.csv_utils.row_type_aggregator import RowTypeAggregator
from gacollector.tasks.csv.base import CsvTask


class SummarizeCsvTask(CsvTask):
    def __init__(self, folder_path, out_file_path=None, picked_columns=None):
        super().__init__(folder_path, out_file_path, picked_columns)
        self.etalon_result_row = None

    def collect_rows(self, filename, input_csv):
        additional_headers = get_additional_fields_for_file(filename)
        result_row = self.get_etalon_row(additional_headers)
        for row in input_csv:
            row.update(additional_headers)
            row = self.csv_set.pick_only_choiced_cols(row)
            result_row = self.increment_row(result_row, row)
        self.csv_set.write_out(result_row)

    def get_etalon_row(self, additional_headers):
        if self.etalon_result_row is None:
            self.etalon_result_row = RowTypeAggregator.get_default_values_in_set(csv_set=self.csv_set)
            # self.etalon_result_row = self.csv_set.pick_only_choiced_cols(self.etalon_result_row)
        copy = self.etalon_result_row.copy()
        copy.update(additional_headers)
        copy = self.csv_set.pick_only_choiced_cols(copy)
        return copy

    def increment_row(self, result_row, row):
        # ADDITIONAL_HEADERS
        return RowTypeAggregator.increment_row_by_row(row=row, row_def=result_row)


if __name__ == '__main__':
    import os

    os.chdir('../../../')
    print(os.path.abspath(os.curdir))
    task = SummarizeCsvTask('../out/test', picked_columns="wEeK, 0, 5,   CPA  ")
    task.run()
    print(os.path.abspath(task.out_file_path))
