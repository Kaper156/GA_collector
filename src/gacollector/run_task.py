from gacollector.config.enums import CsvOutOpEnum
from gacollector.tasks import LastWeekTaskFacade as LastWeekTask
from gacollector.tasks import TaskFacade as Task

new_task = Task(
    # base_url=None,
    # date_from=None,
    # date_to=None,
    # period=None,
    folder_name="./out/test",
    csv_operation=CsvOutOpEnum.SUMMARIZE,
)

# by day from previous week monday to sunday
last_week_task = LastWeekTask(
    base_url='',
    csv_operation=CsvOutOpEnum.CONCATENATE,
)

if __name__ == '__main__':
    new_task.run_available()
    # each_week_task_1.run_available()
    # each_week_task_2.run_available()
