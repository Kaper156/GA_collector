import os
from abc import abstractmethod

from gacollector.misc.csv.csv_set import CsvSet
from gacollector.tasks.base import Task


class CsvTask(Task):
    operation_name = 'standart'

    def __init__(self, folder_path, out_file_path=None, picked_columns=None):
        self.csv_folder = folder_path
        self.out_file_path = out_file_path or self.__generate_out_file_path__()
        self.csv_set = CsvSet(self.csv_folder, self.out_file_path, picked_columns)

    def run(self):
        # Operate with each csv
        for filename, csv_reader in self.csv_set.get_csv_readers():
            self.collect_rows(filename=filename, input_csv=csv_reader)
        self.csv_set.close()

    @abstractmethod
    def collect_rows(self, filename, input_csv):
        raise NotImplementedError()

    def __generate_out_file_path__(self):
        name = f'Results_{os.path.basename(self.csv_folder)}'
        name += self.operation_name + ".csv"
        # res_folder = os.path.join('..', os.path.curdir, 'out', 'results')
        # Put result file in folder result of "out"
        res_folder = os.path.join(*os.path.split(self.csv_folder)[:-1], 'results')
        if not os.path.exists(res_folder):
            os.makedirs(res_folder)

        return os.path.join(res_folder, name)
