import base64
import hashlib
import os

from check_csv_and_url import url_get_date
from secret_settings import *


def get_small_hash(value, d1: datetime.datetime, d2: datetime.datetime, DT: int):
    value += str(d1.timestamp()) + str(d2.timestamp()) + str(DT)
    d = hashlib.md5(value.encode('utf-8')).digest()
    d = base64.b64encode(d)
    h = str(d.decode('utf-8'))[:10]
    h = h.replace('/', '')
    h = h.replace(',', '')
    h = h.replace('\\', '')
    return h


def load_filters(f_path):
    with open(f_path, 'rt') as filters_txt:
        return [f.strip() for f in filters_txt if f.strip()]


def save_filters(filters):
    with open('filters.txt', 'wt') as filters_txt:
        for ft in filters:
            filters_txt.write(f"{ft.strip()}\n")


def generate_folder_name(url, d_from, d_to, d_type):
    f_name = datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d_")
    f_name += get_small_hash(url, d_from, d_to, d_type)
    f_name = os.path.join(os.getcwd(), 'out', f_name)
    return f_name


# Set default values
LEVEL_WORK = LEVEL_WORK or LW_URLS
FROM_DATE = FROM_DATE or datetime.datetime.strptime(url_get_date(BASE_URL)[0], '%Y%m%d')
TO_DATE = TO_DATE or datetime.datetime.now()
FOLDER_NAME = FOLDER_NAME or generate_folder_name(BASE_URL, FROM_DATE, TO_DATE, DATE_TYPE)
FILTERS_PATH = FILTERS_PATH or 'filters.txt'
FILTERS = load_filters(FILTERS_PATH)
