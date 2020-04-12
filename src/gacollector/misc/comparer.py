import os

from gacollector.settings.constants import reURL, reFILE


class DateExtractor:
    @classmethod
    def url_get_date(cls, url):
        return reURL.search(url).groups()

    @classmethod
    def file_get_date(cls, filename):
        return reFILE.search(filename).groups()


def get_incorrect_files(urls, download_dir):
    result = list()
    file_dates = ([DateExtractor.file_get_date(file) for file in os.listdir(download_dir)])
    for url in urls:
        if DateExtractor.url_get_date(url) not in file_dates:
            result.append(url)
    return result
