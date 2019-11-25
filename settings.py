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


def generate_folder_name(url, d_from, d_to, d_type):
    f_name = datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d_")
    f_name += get_small_hash(url, d_from, d_to, d_type)
    f_name = os.path.join(os.getcwd(), 'out', f_name)
    return f_name


def generate_out_csv_path(folder_name, out_operation):
    name = f'Results_{os.path.basename(folder_name)}'
    if out_operation == CSV_SUMMARIZE_PERIOD:
        name += '__total_sum.csv'
    else:
        name += '__aggregated_rows.csv'
    res_folder = os.path.join(os.getcwd(), 'out', 'results')
    if not os.path.exists(res_folder):
        os.makedirs(res_folder)

    return os.path.join(res_folder, name)


# Set default values
LEVEL_WORK = LEVEL_WORK or LW_GENERATE_URLS
FROM_DATE = FROM_DATE or datetime.datetime.strptime(url_get_date(BASE_URL)[0], '%Y%m%d')
TO_DATE = TO_DATE or datetime.datetime.now()
FOLDER_NAME = FOLDER_NAME or generate_folder_name(BASE_URL, FROM_DATE, TO_DATE, DATE_TYPE)
OUT_OPERATION = OUT_OPERATION or CSV_OVERALL
OUT_CSV_PATH = OUT_CSV_PATH or generate_out_csv_path(FOLDER_NAME, OUT_OPERATION)
GSHEET_RANGE = GSHEET_RANGE or 'A1'
