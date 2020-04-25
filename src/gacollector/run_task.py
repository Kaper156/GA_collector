from datetime import datetime

from gacollector.config.enums import CsvOutOpEnum, PeriodEnum
from gacollector.tasks import LastWeekTaskFacade as LastWeekTask
from gacollector.tasks import TaskFacade as Task

new_task = Task(
    base_url='',
    date_from=datetime(2020, 4, 13),
    date_to=datetime(2020, 4, 19),
    period=PeriodEnum.DAY,
    # folder_name="./out/test",
    csv_operation=CsvOutOpEnum.SUMMARIZE,
)

# by day from previous week monday to sunday
last_week_task = LastWeekTask(
    base_url='',
    csv_operation=CsvOutOpEnum.SUMMARIZE,
    picked_columns='From,Insertion,Conversions,Value'
)

if __name__ == '__main__':
    new_task.run_available()
    # last_week_task.run_available()
    # each_week_task_1.run_available()
    # each_week_task_2.run_available()
