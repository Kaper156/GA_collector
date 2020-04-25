import csv

from gacollector.misc.csv.helpers import get_additional_fields_for_file
from gacollector.tasks.csv.base import CsvTask


class ConcatenateCsvTask(CsvTask):
    def collect_rows(self, filename, input_csv: csv.DictReader):
        additional_values = get_additional_fields_for_file(filename)
        for row in input_csv:
            row.update(additional_values)
            row = self.csv_set.pick_only_choiced_cols(row)
            self.csv_set.write_out(row)


if __name__ == '__main__':
    import os

    os.chdir('../../../')
    print(os.path.abspath(os.curdir))
    task = ConcatenateCsvTask('../out/test', picked_columns="0, 5,   CPA  , wEeK ")
    task.run()
    print(os.path.abspath(task.out_file_path))
