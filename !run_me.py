from check_csv_and_url import get_undownloaded_urls
from compile import csv_out_gen_sum, csv_out_gen_increment
from sel_new import manage_weeks
from settings import *
from url_generator import generate_urls

# Настройка
# Решетка "#" это знак комментария, поставь, чтобы функция не работала (пропусть функцию)


# Настрой ЗДЕСЬ!!!
# Решетка "#" это знак комментария, поставь, чтобы функция не работала (пропусть функцию)

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

    # os.mkdir(FOLDER_NAME)
    # wait_cookies(FOLDER_NAME)
    # manage_weeks(urls[0], FOLDER_NAME)  # For set download_folder
    # input("Нажмите энтер, после указания папки сохранения")
    while len(urls):
        manage_weeks(urls, FOLDER_NAME, False)
        urls = get_undownloaded_urls(urls, FOLDER_NAME)

    if AVG_CSV:
        csv_out_gen_sum(FOLDER_NAME, FILTERS)
    else:
        csv_out_gen_increment(FOLDER_NAME, FILTERS)
