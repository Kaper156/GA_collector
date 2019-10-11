import os
import re

reURL = re.compile(r"(2\d{3}[0-1]\d[0-3]\d)(?:&|&amp;)_u\.date01=(2\d{3}[0-1]\d[0-3]\d)")
reFILE = re.compile(r"(2\d{3}[0-1]\d[0-3]\d)-(2\d{3}[0-1]\d[0-3]\d)")


def url_get_date(url):
    return reURL.search(url).groups()


def file_get_date(filename):
    return reFILE.search(filename).groups()


def get_undownloaded_urls(urls, download_dir):
    file_dates = ([file_get_date(file) for file in os.listdir(download_dir)])
    for url in urls:
        if url_get_date(url) not in file_dates:
            yield url
