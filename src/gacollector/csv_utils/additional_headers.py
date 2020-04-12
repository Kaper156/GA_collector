import datetime

from gacollector.misc.comparer import DateExtractor
from gacollector.settings.constants import DATE_OUT_FORMAT


def get_additional_fields_for_file(filename):
    # Warning rewrite it if additional headers changed
    d1, d2 = DateExtractor.file_get_date(filename)
    d1, d2 = [datetime.datetime.strptime(d, "%Y%m%d") for d in (d1, d2)]
    week = d2.strftime("%V")
    is_week = f'{d1.year}{week}'
    if week == '01':  # If date_from is in previous year, but week started as first week in next year
        is_week = f'{d2.year}{week}'
    return {
        "From": d1.strftime(DATE_OUT_FORMAT),
        "To": d2.strftime(DATE_OUT_FORMAT),
        "Week": is_week
    }
