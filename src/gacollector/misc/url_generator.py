import calendar
import datetime

from gacollector.settings.constants import reURL
from gacollector.settings.constants import tmpl_date1, tmpl_date2
from gacollector.settings.enums import PeriodEnum


def add_month(date1):
    day = calendar.monthrange(date1.year, date1.month)[1]
    return datetime.datetime(date1.year, date1.month, day=day)


def add_week(date1):
    return date1 + datetime.timedelta(days=6)


def add_day(date1):
    return date1


def put_dates(url, date1, date2):
    url = url.replace(tmpl_date1, date1.strftime("%Y%m%d"))
    url = url.replace(tmpl_date2, date2.strftime("%Y%m%d"))
    return url


def range_generator(d_from, d_to, incr_function):
    cur_date_1 = d_from
    cur_date_2 = None
    while True:
        cur_date_2 = incr_function(cur_date_1)
        if cur_date_2 >= d_to:
            cur_date_2 = d_to
            yield cur_date_1, cur_date_2
            break

        yield cur_date_1, cur_date_2
        cur_date_1 = cur_date_2 + datetime.timedelta(days=1)


TYPES = {
    PeriodEnum.DAY: add_day,
    PeriodEnum.WEEK: add_week,
    PeriodEnum.MONTH: add_month
}


# TODO make as list
def generate_urls(src_url, date_from, date_to, date_type: PeriodEnum):
    if date_type not in PeriodEnum:
        raise ValueError("Incorrect date-range value, please select from: TYPE_DAY, TYPE_WEEK, TYPE_MONTH")

    # url_template = re.sub(URL_REGEX, tmpl_date1 + "&_u.date01=" + tmpl_date2, src_url)
    url_template = reURL.sub(tmpl_date1 + "&_u.date01=" + tmpl_date2, src_url)

    date_generator = range_generator(date_from, date_to, TYPES[date_type])

    # with open(TEMPORARY_URLS_PATH, 'wt') as urls_file:
    for date1, date2 in date_generator:
        new_url = put_dates(url_template, date1, date2)
        yield new_url
