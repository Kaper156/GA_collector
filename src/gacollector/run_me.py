from gacollector.collector.csv_collectors import CsvCollector, CsvSummarize
from gacollector.connectors.google_sheets_api.main import Gsheet
from gacollector.misc.comparer import get_undownloaded_urls
from gacollector.misc.url_generator import generate_urls
from gacollector.selen.scenario import BrowserScenario
from gacollector.settings.settings import *

if __name__ == '__main__':
    if LEVEL_WORK >= LW_GENERATE_URLS:
        # Генерирует ссылки в файл urls.txt
        generate_urls(BASE_URL=BASE_URL,
                      FROM_DATE=FROM_DATE, TO_DATE=TO_DATE,
                      DATE_TYPE=DATE_TYPE
                      )

    # Читает ссылки из файла urls.txt
    with open(TEMPORARY_URLS_PATH, "rt") as f:
        urls = [l.strip() for l in f.readlines()]
    undownloaded_urls = urls.copy()
    if LEVEL_WORK >= LW_DOWNLOAD_GENERATED_URLS:
        # Создаем или проверяем папку для загурзки
        try:
            os.makedirs(FOLDER_NAME)
            print(f"Создал папку: \t{os.path.abspath(FOLDER_NAME)}")
        except FileExistsError:
            # Если папка уже существует, то проверить файлы в ней
            print(f"Нашёл папку: \t{os.path.abspath(FOLDER_NAME)}")
            undownloaded_urls = get_undownloaded_urls(urls, FOLDER_NAME)
            print(f"В ней найденно {len(urls) - len(undownloaded_urls)} скачанных файлов")

        if len(undownloaded_urls):
            # Работаем с браузером
            with BrowserScenario(FOLDER_NAME, PROFILE_PATH) as bs:
                # Пока остаются ссылки
                while len(undownloaded_urls):
                    print("Проверяю ссылки и файлы...")
                    undownloaded_urls = get_undownloaded_urls(urls, FOLDER_NAME)
                    print(f"Осталось ещё {len(undownloaded_urls)}")
                    cnt = 0
                    for url in undownloaded_urls:
                        cnt += 1
                        percent = ((len(urls) - (len(undownloaded_urls) - cnt)) / len(urls)) * 100
                        period = url_get_date(url)
                        print(
                            f"[{cnt} из {len(undownloaded_urls)}({len(urls)})] (Скачано {round(percent, 2):3,.2f}%) \t"
                            f"Скачиваю csv за период {period[0]} - {period[1]}")
                        bs.get_week_data(url)
                print(f"Csv успешно скачаны")
    if LEVEL_WORK >= LW_COLLECT_RESULT:
        operator = None
        if OUT_OPERATION == CSV_SUMMARIZE_PERIOD:
            operator = CsvSummarize(folder_with_csv=FOLDER_NAME, out_file_path=OUT_CSV_PATH)
        else:
            operator = CsvCollector(folder_with_csv=FOLDER_NAME, out_file_path=OUT_CSV_PATH)
        operator.write_out_csv()
    if LEVEL_WORK >= LW_SEND_TO_GOOGLE_SHEETS and GSHEET_SPREADSHEET:
        print("Авторизовываемся в google-sheets-api...")
        gsheet = Gsheet()
        print("Посылаем данные..")
        updated_rows_count = gsheet.send_from_csv(OUT_CSV_PATH, GSHEET_SPREADSHEET, GSHEET_RANGE)
        print(f"Обновленно {updated_rows_count} строк")
