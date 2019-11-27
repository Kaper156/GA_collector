import base64
import csv
import datetime
import hashlib
import os
import random
from decimal import Decimal

csv.register_dialect('ga',
                     quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)

_filter = "Last touch Imp Conversions,Last touch Imp Conversion Value,Last touch Click Conversions,Last touch Click " \
          "Conversion Value,% Change in Conversions from Last touch Imp to Last touch Click".split(',')

d_fmt = '%Y%m%d'
rows = [
    {
        'title': 'Line item',
        'type': 'str',
        'length': 20,
    },
    {
        'title': 'Last touch Imp Conversions',
        'type': 'int.00',
        'between': (0, 200)
    },
    {
        'title': 'Last touch Imp Conversion Value',
        'type': 'dollar_US',
        'between': (0, 100 * 1000)
    },
    {
        'title': 'Last touch Click Conversions',
        'type': 'int.00',
        'between': (0, 100 * 1000)
    },
    {
        'title': 'Last touch Click Conversion Value',
        'type': 'dollar_US',
        'between': (0, 100 * 1000)
    },
    {
        'title': '% Change in Conversions from Last touch Imp to Last touch Click',
        'type': 'percent',
        'can_be_negative': True
    },
]


def __decimal_to_str__(val):
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US')
    # locale.setlocale(locale.LC_MONETARY, "en_US")
    return locale.currency(val, grouping=True)


def get_hash():
    value = datetime.datetime.now()
    value = value.isoformat()
    d = hashlib.md5(value.encode('utf-8')).digest()
    d = base64.b64encode(d)
    h = str(d.decode('utf-8'))
    h = h.replace('/', '')
    h = h.replace(',', '')
    h = h.replace('\\', '')
    return h


def generate_int00(row_def):
    value = random.randint(*row_def['between'])
    return f"{value:00f}"


def generate_dollar_US(row_def):
    value = float(random.randint(*row_def['between']) + random.random())
    value = Decimal(value)
    return __decimal_to_str__(value)


def generate_percent(row_def):
    value = random.randint(0, 100)
    if row_def['can_be_negative']:
        value *= random.choice([1, -1])
    return f"{value}%"


def generate_str(row_def):
    return get_hash()[:row_def['length']]


def generate_row(rows):
    result = list()
    table = {
        'percent': generate_percent,
        'dollar_US': generate_dollar_US,
        'int.00': generate_int00,
        'str': generate_str
    }
    for row in rows:
        result.append(table[row['type']](row))
    return result


def gen_comments(d1: datetime.datetime, d2: datetime.datetime):
    return [
        ['# ' + '-' * 15],
        ['# ' + get_hash()],
        ['# ' + get_hash()],
        ['# ' + d1.strftime(d_fmt) + '-' + d2.strftime(d_fmt)],
        ['# ' + '-' * 15],
    ]


def generate_csv(rows, path, d1: datetime.datetime, d2: datetime.datetime, row_len=20):
    with open(path, 'w', newline='', encoding='utf-8') as _f:
        writer = csv.writer(_f, dialect='ga')
        # Comments
        # _f.writelines(gen_comments(d1, d2))
        for com in gen_comments(d1, d2):
            writer.writerow(com)

        writer.writerow('')

        # Header row
        header = [row['title'] for row in rows]
        writer.writerow(header)

        # Data row
        for i in range(row_len):
            writer.writerow(generate_row(rows))

        writer.writerow('')

        # Sum row
        writer.writerow(_filter)
        writer.writerow([0] * len(_filter))
        writer.writerow([0] * len(_filter))


# date_range: iter of tuples with two dates
# Ex: [ (2015-02-04, 2019-06-09), ...]
def generate_csv_for_range(rows_def, date_range, folder):
    for item in date_range:
        dr = item[0].strftime(d_fmt) + "-" + item[1].strftime(d_fmt)
        name = os.path.join(folder, 'Analytics Model Comparison Tool ' + dr + '.csv')
        row_len = random.randint(20, 50)
        generate_csv(rows_def, name, item[0], item[1], row_len)


if __name__ == '__main__':
    folder = os.path.join('.', 'week')
    d1 = datetime.datetime(2018, 1, 1)
    d2 = d1 + datetime.timedelta(days=6)
    dr = list()
    for i in range(2):
        dr.append((d1, d2))
        d1 = d2 + datetime.timedelta(days=1)
        d2 = d1 + datetime.timedelta(days=6)

    generate_csv_for_range(rows, dr, folder)

    # generate_csv(rows=rows, path='1.csv',
    #              d1=datetime.datetime(2015, 2, 3), d2=datetime.datetime(2016, 3, 4),
    #              row_len=40)
