import base64
import datetime
import hashlib
import os

from check_csv_and_url import url_get_date
from url_generator import TYPE_MONTH, TYPE_WEEK, TYPE_DAY

LW_URLS = 3
LW_CHECK_FOLDER = 2
LW_AVG_FILE = 1

LEVEL_WORK = LW_URLS

BASE_URL = "https://analytics.google.com/analytics/web/?authuser=1#/report/bf-roi-calculator"

FROM_DATE = datetime.datetime.strptime(url_get_date(BASE_URL)[0], '%Y%m%d')
# FROM_DATE = datetime.datetime(year=2018, month=8, day=1)

TO_DATE = datetime.datetime(year=2019, month=7, day=31)
# TO_DATE = datetime.datetime.now()

# Для типа периода используй TYPE_DAY или TYPE_MONTH или TYPE_WEEK
DATE_TYPE = TYPE_WEEK  # TYPE_DAY TYPE_WEEK TYPE_MONTH

AVG_CSV = False


def get_small_hash(value, d1: datetime.datetime, d2: datetime.datetime, DT: int):
    value += str(d1.timestamp()) + str(d2.timestamp()) + str(DT)
    d = hashlib.md5(value.encode('utf-8')).digest()
    d = base64.b64encode(d)
    h = str(d.decode('utf-8'))[:10]
    h = h.replace('/', '')
    h = h.replace(',', '')
    h = h.replace('\\', '')
    return h


# При остром желании поменяй FOLDER_NAME на любой путь, например:
FOLDER_NAME = datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d_")
FOLDER_NAME += get_small_hash(BASE_URL, FROM_DATE, TO_DATE, DATE_TYPE)
FOLDER_NAME = os.path.join(os.getcwd(), 'out', FOLDER_NAME)


def FILTERS():
    with open('filters.txt', 'rt') as filters_txt:
        return [f + "\n" for f in filters_txt]


# Используй только такой слэш '/'
PROFILE_PATH = "C:/Users/User/AppData/Roaming/Mozilla/Firefox/Profiles/47kb4fzr.SeleniumTestProfile"

# Флаг проверки авторизации; Если True то ожидать авторизации перед загрузкой
IS_AUTH_NEEDED = True
