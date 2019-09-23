import codecs
import csv
import datetime
import os
from decimal import Decimal, DecimalException

from check_csv_and_url import file_get_date

ADDITIONAL_HEADERS = ["Week", "From", "To"]
csv.register_dialect('ga',
                     quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)

str_to_decimal = lambda val: val.replace('$', '').replace(',', '').replace(' ', '')


def decimal_to_str(val):
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US')
    # locale.setlocale(locale.LC_MONETARY, "en_US")
    return locale.currency(val, grouping=True)


def get_outcsv_filename(download_folder):
    out_dir_path = os.path.join(os.getcwd(), "out")
    out_csv_path = os.path.basename(download_folder) + ".csv"
    out_csv_path = os.path.join(out_dir_path, out_csv_path)
    if not os.path.exists(out_dir_path):
        os.mkdir(out_dir_path)
    return out_csv_path


def filter_generator(filters):
    def user_filter(iterator):
        for line in iterator:
            if line[:1] == '#':
                continue
            if not line.strip():
                continue
            if line in filters:
                break
            yield line

    return user_filter


# Yield header row, after this yield tuple([rows], filename)
# Rows are filtered
def csv_out_gen_rows(download_folder, filters: list):
    filter_func = filter_generator(filters)
    header_returned = False
    for file_name in os.listdir(download_folder):
        with codecs.open(os.path.join(download_folder, file_name), encoding='windows-1251') as file:
            csv_dict = csv.DictReader(filter_func(file), dialect="ga")
            if not header_returned:
                yield csv_dict.fieldnames
                header_returned = True
            yield csv_dict, file_name


def add_additional_values_in_row(row, filename):
    d1, d2 = file_get_date(filename)
    d1, d2 = [datetime.datetime.strptime(d, "%Y%m%d") for d in (d1, d2)]
    week = d2.strftime("%V")
    is_week = f'{d1.year}{week}'
    if week == '01':
        is_week = f'{d2.year}{week}'  # TODO Comment here
    row.update({
        "From": d1.strftime("%Y.%m.%d"),
        "To": d2.strftime("%Y.%m.%d"),
        "Week": is_week
    })
    return row


def try_parse_default_values(row: csv.OrderedDict):
    if (None in row.values()) | ('-' in row.values()):
        return None
    for col in row.keys():
        val = row[col]
        if '$' in val:
            try:
                Decimal(str_to_decimal(val))
                yield col, Decimal()
                continue
            except DecimalException:
                pass
        try:
            int(val)
            yield col, int(0)
            continue
        except ValueError:
            pass
        try:
            float(val)
            yield col, float(0.0)
            continue
        except ValueError:
            yield col, str('-')


def set_row_defaults(download_folder, filters: list):
    files = csv_out_gen_rows(download_folder, filters)
    next(files)  # Skip header
    types = None
    while types is None:
        types = try_parse_default_values(next(next(files)[0]))
    del files
    return csv.OrderedDict(types)


def avg_row_to_string_values(avg_row: csv.OrderedDict):
    for col in avg_row.keys():
        if type(avg_row[col]) is Decimal:
            avg_row[col] = decimal_to_str(avg_row[col])
    return avg_row


def csv_out_gen_increment(download_folder, filters: list):
    file_gen = csv_out_gen_rows(download_folder, filters)
    with open(get_outcsv_filename(download_folder), 'wt', newline="") as f:
        header = next(file_gen)
        header += ADDITIONAL_HEADERS
        csv_dict = csv.DictWriter(f, header, dialect="ga")
        csv_dict.writeheader()
        for file, filename in file_gen:
            for row in file:
                row = add_additional_values_in_row(row, filename)
                csv_dict.writerow(row)


def csv_out_gen_sum(download_folder, filters: list):
    file_gen = csv_out_gen_rows(download_folder, filters)
    types = set_row_defaults(download_folder, filters)

    with open(get_outcsv_filename(download_folder), 'wt', newline="") as f:
        header = next(file_gen)
        header += ADDITIONAL_HEADERS
        csv_dict = csv.DictWriter(f, header, dialect="ga")
        csv_dict.writeheader()
        for file, filename in file_gen:
            avg_row = csv.OrderedDict(types)
            for row in file:
                for col in row.keys():
                    if col in ADDITIONAL_HEADERS:
                        continue
                    _type = type(types[col])
                    if _type in (str, None):
                        continue

                    val = row[col]
                    if _type is Decimal:
                        val = str_to_decimal(val)
                    avg_row[col] += _type(val)
            avg_row = add_additional_values_in_row(avg_row, filename)
            csv_dict.writerow(avg_row_to_string_values(avg_row))


if __name__ == '__main__':
    filters = [
        "Last touch Imp Conversions,Last touch Imp Conversion Value,Last touch Click Conversions,Last touch Click Conversion Value,% Change in Conversions from Last touch Imp to Last touch Click"

    ]
    filters = [f + "\n" for f in filters]
    # csv_out_gen_increment("GA_test_days", FILTERS)
    csv_out_gen_sum("GA_test_days", filters)
