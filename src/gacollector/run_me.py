from time import sleep

from gacollector.checkers.base import CsvFileChecker
from gacollector.connectors.google_sheets_api.main import Gsheet
from gacollector.csv_utils.overall import CsvCollector
from gacollector.csv_utils.summarize import CsvSummarize
from gacollector.misc.url_generator import generate_urls
from gacollector.selen.scenario import BrowserScenario
from gacollector.settings.settings import *

if __name__ == '__main__':

    urls = list(generate_urls(src_url=BASE_URL,
                              date_from=FROM_DATE, date_to=TO_DATE,
                              date_type=DATE_TYPE
                              ))
    incomplete_urls = urls.copy()
    checker = CsvFileChecker(FOLDER_NAME)
    if LEVEL_WORK >= LevelWorkEnum.DOWNLOAD_GENERATED_URLS:

        # Создаем или проверяем папку для загурзки
        try:
            os.makedirs(FOLDER_NAME)
            print(f"Создал папку: \t{os.path.abspath(FOLDER_NAME)}")
        except FileExistsError:
            # Если папка уже существует, то проверить файлы в ней
            print(f"Нашёл папку: \t{os.path.abspath(FOLDER_NAME)}")
            incomplete_urls = checker.get_incomplete_urls(urls)
            print(f"В ней найденно {len(urls) - len(incomplete_urls)} скачанных файлов")

        if len(incomplete_urls):
            # Работаем с браузером
            with BrowserScenario(FOLDER_NAME, PROFILE_PATH) as bs:
                # Пока остаются ссылки
                while len(incomplete_urls):
                    print("Проверяю ссылки и файлы...")
                    sleep(3)
                    incomplete_urls = checker.get_incomplete_urls(urls)
                    print(f"Осталось ещё {len(incomplete_urls)}")
                    cnt = 0
                    for url in incomplete_urls:
                        cnt += 1
                        percent = ((len(urls) - (len(incomplete_urls) - cnt)) / len(urls)) * 100
                        period = DateExtractor.url_get_date(url)
                        print(
                            f"[{cnt} из {len(incomplete_urls)}({len(urls)})] (Скачано {round(percent, 2):3,.2f}%) \t"
                            f"Скачиваю csv за период {period[0]} - {period[1]}")
                        bs.get_week_data(url)
                print(f"Csv успешно скачаны")
    if LEVEL_WORK >= LevelWorkEnum.COLLECT_RESULT:
        checker.delete_duplicates()
        checker.delete_invalid_files()
        operator = None
        if OUT_OPERATION == CsvOutOpEnum.SUMMARIZE_PERIOD:
            operator = CsvSummarize(folder_with_csv=FOLDER_NAME, out_file_path=OUT_CSV_PATH)
        else:
            operator = CsvCollector(folder_with_csv=FOLDER_NAME, out_file_path=OUT_CSV_PATH)
        print(os.path.abspath(os.curdir))
        operator.write_out_csv()
    if LEVEL_WORK >= LevelWorkEnum.SEND_TO_GOOGLE_SHEETS and GSHEET_SPREADSHEET:
        print("Авторизовываемся в google-sheets-api...")
        gsheet = Gsheet()
        print("Посылаем данные..")
        updated_rows_count = gsheet.send_from_csv(OUT_CSV_PATH, GSHEET_SPREADSHEET, GSHEET_RANGE)
        print(f"Обновленно {updated_rows_count} строк")
