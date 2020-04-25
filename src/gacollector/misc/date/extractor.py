from gacollector.config.constants import reURL, reFILE


class DateExtractor:
    @classmethod
    def url_get_date(cls, url):
        return reURL.search(url).groups()

    @classmethod
    def file_get_date(cls, filename):
        return reFILE.search(filename).groups()
