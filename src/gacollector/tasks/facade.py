from gacollector.config.enums import CsvOutOpEnum, PeriodEnum
from gacollector.misc.date.week import get_previous_week_range
from gacollector.misc.files.paths import up_to_project_folder, get_folder_path_from_name
from gacollector.tasks import DownloadTask, ConcatenateCsvTask, SummarizeCsvTask
from gacollector.tasks.gsheet import GsheetTask


class TaskFacade:
    def __init__(self, base_url=None, date_from=None, date_to=None, period=PeriodEnum.DAY,
                 folder_name=None,
                 csv_operation=CsvOutOpEnum.CONCATENATE, out_csv_path=None,
                 gsheet_id=None, gsheet_cell_address=None):
        self.base_url = base_url
        self.date_from = date_from
        self.date_to = date_to
        self.period = period

        up_to_project_folder()
        self.folder_path = get_folder_path_from_name(folder_name)
        self.csv_operation = csv_operation
        self.out_csv_path = out_csv_path

        self.gsheet_id = gsheet_id
        self.gsheet_cell_address = gsheet_cell_address

    def run_available(self):
        for task_cls, params in self.generate_schedule():
            print('*' * 20)
            print(f"Task {task_cls.__name__} started")
            task = task_cls(**params)
            task.run()
            if task_cls is DownloadTask:
                self.folder_path = task.get_folder_path()
            if task_cls is ConcatenateCsvTask or task_cls is SummarizeCsvTask:
                self.out_csv_path = task.out_file_path
            print(f"Task \"{task_cls.__name__}\" is completed")

    def generate_schedule(self):
        task = None
        if None not in (self.base_url,):
            task = [DownloadTask, {'base_url': self.base_url,
                                   'date_from': self.__dict__.get('date_from', None),
                                   'date_to': self.__dict__.get('date_to', None),
                                   'folder_name': self.__dict__.get('folder_path', None),
                                   }]

            yield task
        if None not in (self.csv_operation,):
            cls = None
            if self.csv_operation == CsvOutOpEnum.CONCATENATE:
                cls = ConcatenateCsvTask
            elif self.csv_operation == CsvOutOpEnum.SUMMARIZE:
                cls = SummarizeCsvTask
            else:
                raise Exception(f"I don't know about {self.csv_operation} csv-operation")
            task = [cls, {'folder_path': self.__dict__.get('folder_path', None)}]
            yield task
        if None not in (self.gsheet_id,):
            task = [GsheetTask, {'out_csv_path': self.out_csv_path,
                                 'gsheet_id': self.gsheet_id,
                                 'gsheet_cell_address': self.gsheet_cell_address}]
            yield task


class LastWeekTaskFacade(TaskFacade):
    def __init__(self, base_url, current_date=None,
                 out_csv_path=None, csv_operation=CsvOutOpEnum.CONCATENATE,
                 gsheet_id=None, gsheet_cell_address=None):
        d1, d2 = get_previous_week_range(current_date)
        super().__init__(base_url=base_url, date_from=d1, date_to=d2, period=PeriodEnum.DAY,
                         csv_operation=csv_operation, out_csv_path=out_csv_path,
                         gsheet_id=gsheet_id, gsheet_cell_address=gsheet_cell_address)
