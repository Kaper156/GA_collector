from check_csv_and_url import get_undownloaded_urls
from compile import csv_out_gen_sum, csv_out_gen_increment
from sel_new import manage_weeks
from settings import *
from url_generator import generate_urls


if __name__ == '__main__':
    # Генерирует ссылки в файл urls.txt
    generate_urls(
        BASE_URL=BASE_URL
        , FROM_DATE=FROM_DATE
        , TO_DATE=TO_DATE
        , DATE_TYPE=DATE_TYPE
    )

    # Кстати, можешь добавить ссылки если вдруг захочешь в файл urls.txt

    # Читает ссылки из файла urls.txt
    with open("urls.txt", "rt") as f:
        urls = [l.strip() for l in f.readlines()]

    os.mkdir(FOLDER_NAME)
    is_first_time = True
    while len(urls):
        manage_weeks(urls, FOLDER_NAME, is_first_time)
        urls = get_undownloaded_urls(urls, FOLDER_NAME)
        is_first_time = False
        break
    exit()
    if AVG_CSV:
        csv_out_gen_sum(FOLDER_NAME, FILTERS)
    else:
        csv_out_gen_increment(FOLDER_NAME, FILTERS)
