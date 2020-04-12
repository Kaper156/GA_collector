import base64
import datetime
import hashlib
import os

from gacollector.settings.enums import PeriodEnum


def get_small_hash(value, d1: datetime.datetime, d2: datetime.datetime, DT: int):
    value += str(d1.timestamp()) + str(d2.timestamp()) + str(DT)
    d = hashlib.md5(value.encode('utf-8')).digest()
    d = base64.b64encode(d)
    h = str(d.decode('utf-8'))[:10]
    h = h.replace('/', '')
    h = h.replace(',', '')
    h = h.replace('\\', '')
    return h


def generate_folder_name(url=None, d_from=None, d_to=None, d_type=PeriodEnum.DAY):
    if url is None:
        url = ''
    if d_from is None:
        d_from = datetime.datetime.now() - datetime.timedelta(days=1)
    if d_to is None:
        d_to = datetime.datetime.now()
    f_name = datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d_")
    f_name += get_small_hash(url, d_from, d_to, d_type)
    f_name = os.path.join(os.getcwd(), 'out', f_name)
    return f_name
