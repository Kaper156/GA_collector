from check_csv_and_url import get_undownloaded_urls
from compile import csv_out_gen_sum, csv_out_gen_increment, csv_out_uniq_line_items
from sel_new import BrowserScenario
from settings import *
from url_generator import generate_urls

if __name__ == '__main__':
    # Генерирует ссылки в файл urls.txt
    generate_urls(BASE_URL=BASE_URL,
                  FROM_DATE=FROM_DATE, TO_DATE=TO_DATE,
                  DATE_TYPE=DATE_TYPE
                  )

    # Читает ссылки из файла urls.txt
    with open("urls.txt", "rt") as f:
        urls = [l.strip() for l in f.readlines()]

    # Создаем папку для загурзки
    os.mkdir(FOLDER_NAME)

    # Работаем с браузером
    with BrowserScenario(FOLDER_NAME, PROFILE_PATH, IS_AUTH_NEEDED) as bs:
        # Пока остаются ссылки
        while len(urls):
            for url in urls:
                bs.get_week_data(url)
            # Собираем пропущенные ссылки
            urls = get_undownloaded_urls(urls, FOLDER_NAME)
            bs.is_authorization_needed = False

    if AVG_CSV:
        csv_out_gen_sum(FOLDER_NAME, FILTERS)
    else:
        csv_out_gen_increment(FOLDER_NAME, FILTERS)
    csv_out_uniq_line_items(FOLDER_NAME, FILTERS)
