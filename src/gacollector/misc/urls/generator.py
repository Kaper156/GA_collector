from gacollector.config.constants import reURL
from gacollector.config.constants import tmpl_date1, tmpl_date2
from gacollector.config.enums import PeriodEnum
from gacollector.misc.date.incrementor import DateIncrementer


class UrlGenerator:
    @classmethod
    def generate_urls(cls, src_url, date_from, date_to, date_type: PeriodEnum):
        url_template = reURL.sub(tmpl_date1 + "&_u.date01=" + tmpl_date2, src_url)
        date_generator = DateIncrementer.range_generator(date_from, date_to, date_type)

        for date1, date2 in date_generator:
            new_url = cls.put_dates(url_template, date1, date2)
            yield new_url

    @staticmethod
    def put_dates(url, date1, date2):
        url = url.replace(tmpl_date1, date1.strftime("%Y%m%d"))
        url = url.replace(tmpl_date2, date2.strftime("%Y%m%d"))
        return url
