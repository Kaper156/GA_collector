import calendar
import datetime

TYPE_DAY = 1
TYPE_WEEK = 7
TYPE_MONTH = 30

tmpl_date1 = "<!#@!1>"
tmpl_date2 = "<!#@!2>"


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
    TYPE_DAY: add_day,
    TYPE_WEEK: add_week,
    TYPE_MONTH: add_month
}


def generate_urls(BASE_URL, FROM_DATE, TO_DATE, DATE_TYPE):
    if DATE_TYPE not in [TYPE_DAY, TYPE_WEEK, TYPE_MONTH]:
        print("ТИП ПЕРИОДА НЕ ВЕРНЫЙ!!!!!!! ПОдставь из TYPE_DAY, TYPE_WEEK, TYPE_MONTH")
        return
    import re

    url_template = re.sub(r"2\d{3}[0-1]\d[0-3]\d(&|&amp;)_u\.date01=2\d{3}[0-1]\d[0-3]\d",
                          tmpl_date1 + "&_u.date01=" + tmpl_date2, BASE_URL)
    urls = list()

    date_generator = range_generator(FROM_DATE, TO_DATE, TYPES[DATE_TYPE])

    with open("urls.txt", 'wt') as urls_file:
        for date1, date2 in date_generator:
            new_url = put_dates(url_template, date1, date2)
            urls_file.write(f"{new_url}\n")
            # print(new_url)
            urls.append(new_url)
    print(f"Созданно {len(urls)} ссылок")

