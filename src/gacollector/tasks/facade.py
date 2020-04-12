from gacollector.settings.enums import CsvOutOpEnum, PeriodEnum
from gacollector.tasks import DownloadTask, ConcatenateCsvTask, SummarizeCsvTask


class TaskFacade:
    def __init__(self, base_url=None, date_from=None, date_to=None, period=PeriodEnum.DAY,
                 folder_name=None,
                 csv_operation=CsvOutOpEnum.OVERALL, out_csv_path=None,
                 gsheet_id=None, gsheet_cell_address=None):
        self.base_url = base_url
        self.date_from = date_from
        self.date_to = date_to
        self.period = period

        self.folder_path = self.__get_folder_path_from_name__(folder_name)
        self.csv_operation = csv_operation
        self.out_csv_path = out_csv_path

        self.gsheet_id = gsheet_id
        self.gsheet_cell_address = gsheet_cell_address

        self.available_task = list()
        self.update_available()

    def print_available(self):
        print(self.available_task)

    def run_available(self):
        for task_cls, params in self.available_task:
            print(task_cls)
            task = task_cls(**params)
            task.run()
            if task_cls is DownloadTask:
                self.folder_path = task.get_folder_path()
            print(f"Task \"{task_cls}\" is completed")

    def update_available(self):
        self.available_task = list()
        if None not in (self.base_url,):
            task = [DownloadTask, {'base_url': self.base_url,
                                   'date_from': self.__dict__.get('date_from', None),
                                   'date_to': self.__dict__.get('date_to', None)}]

            if self.folder_path:
                self.available_task[0][1]['folder_name'] = self.folder_path
            self.available_task.append(task)
        if None not in (self.csv_operation,):
            cls = None
            if self.csv_operation == CsvOutOpEnum.OVERALL:
                cls = ConcatenateCsvTask
            elif self.csv_operation == CsvOutOpEnum.SUMMARIZE_PERIOD:
                cls = SummarizeCsvTask
            else:
                raise Exception(f"I don't know about {self.csv_operation} csv-operation")

            print(self.__dict__.get('folder_path', None))

            self.available_task.append([cls, {'folder_path': self.__dict__.get('folder_path', None)}])
        # TODO gsheet task

    @staticmethod
    def __get_folder_path_from_name__(folder_name):
        import os
        if not folder_name:
            return None
        # return if this folder exist
        if os.path.exists(folder_name):
            return os.path.abspath(folder_name)
        # create new folder in GA_Selenium (project-folder)/out
        cur_dir = os.path.abspath(os.path.curdir)
        while not os.path.exists(os.path.join(cur_dir, 'out')):
            cur_dir = os.path.join(cur_dir, '..')
            # print(f"Change dir to: \n{cur_dir}\n{os.path.abspath(cur_dir)}\n\n")  # Debug
        out_dir = os.path.abspath(cur_dir)  # Replace dots with real folder path
        folder_name = os.path.split(folder_name)[-1]  # Get folder name (folder-name may contain some path)
        return os.path.join(out_dir, 'out', folder_name)
