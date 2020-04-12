from gacollector.settings.enums import CsvOutOpEnum
from gacollector.tasks import TaskFacade as Task

new_task = Task(
    # base_url=None,
    # date_from=None,
    # date_to=None,
    # period=None,
    folder_name="./out/test",
    csv_operation=CsvOutOpEnum.SUMMARIZE_PERIOD,

)

# each_week_task_1 = Task(
#     base_url='',
#     date_from=datetime(2020, 1, 31),
#     date_to=datetime(2020, 1, 31),
#     period=PeriodEnum.DAY,
#     folder_name=None,
#     csv_operation=CsvOutOpEnum.OVERALL,
#     out_csv_path=None,
#     gsheet_id='',  # Сейчас не работает
#     gsheet_cell_address='',  # Сейчас не работает
# )
#
# each_week_task_2 = Task(
#     base_url='',
#     date_from=datetime(2020, 1, 31),
#     date_to=datetime(2020, 1, 31),
#     period=PeriodEnum.DAY,
#     folder_name=None,
#     csv_operation=CsvOutOpEnum.OVERALL,
#     out_csv_path=None,
#     gsheet_id='',  # Сейчас не работает
#     gsheet_cell_address='',  # Сейчас не работает
# )

if __name__ == '__main__':
    new_task.run_available()
    # each_week_task_1.run_available()
    # each_week_task_2.run_available()
