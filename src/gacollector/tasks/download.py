import datetime
import os
from time import sleep

from .base import Task
from ..checkers.base import CsvFileChecker
from ..misc.comparer import DateExtractor
from ..misc.folder_name import generate_folder_name
from ..misc.url_generator import generate_urls
from ..selen.scenario import BrowserScenario
from ..settings.enums import PeriodEnum
from ..settings.secret_settings import PROFILE_PATH


class DownloadTask(Task):
    def __init__(self, base_url, date_from=None, date_to=None, period=PeriodEnum.MONTH,
                 folder_to_download=None, force_delete_bad_headers=False):
        if folder_to_download is None:
            folder_to_download = self.__generate_folder_name__()

        self.base_url = base_url
        self.date_from = date_from or datetime.datetime.strptime(DateExtractor.url_get_date(base_url)[0], '%Y%m%d')
        self.date_to = date_to or datetime.datetime.now()
        self.period = period

        self.folder_to_download = None
        self.select_folder(folder_to_download)
        # TODO chenge delete bad headers to move in thrash_folder
        self.file_checker = CsvFileChecker(self.folder_to_download, force_delete_bad_headers)

        # After any change must be None
        self.__all_urls__ = list(generate_urls(self.base_url, self.date_from, self.date_to, self.period))

        # List of file_name, abs_file_path
        self.__files__ = list()

    def run(self):
        # Get only not downloaded urls
        urls = self.file_checker.get_incomplete_urls(self.__all_urls__)

        done_cnt = 0
        all_urls_cnt = len(self.__all_urls__)
        if len(urls) == 0:
            print(f"All urls are already downloaded ({len(urls)}/{all_urls_cnt}) skip task")
            return
        with BrowserScenario(self.folder_to_download, PROFILE_PATH) as bs:
            while len(urls) > 0:
                print(f"Start downloading {len(urls)} csv-files")

                for url in urls:
                    percent = ((all_urls_cnt - done_cnt) / all_urls_cnt) * 100
                    period = DateExtractor.url_get_date(url)
                    print(
                        f"[{done_cnt} из {all_urls_cnt}] (Скачано {round(percent, 2):3,.2f}%) \t"
                        f"Скачиваю csv за период {period[0]} - {period[1]}")
                    bs.get_week_data(url)
                print("Sleep before checking and maybe next iteration")

                # Sleep and wait for last file be downloaded
                sleep(5)
                # TODO Wait while folder contain undownloaded file (ext: .tmp)
                # Delete bad files
                bad_files_count = self.check()
                # Decrement bad from counter
                done_cnt -= bad_files_count
                # Get new url-list without bad files
                urls = self.file_checker.get_incomplete_urls(self.__all_urls__)

    def check(self):
        bad_files_count = 0
        bad_files_count += self.file_checker.delete_duplicates()
        bad_files_count += self.file_checker.delete_invalid_files()
        return bad_files_count

    def select_folder(self, folder_to_download):
        folder_to_download = os.path.abspath(folder_to_download)
        if not os.path.exists(folder_to_download):
            print(f"Create folder: \t{folder_to_download}")
            os.mkdir(folder_to_download)
        self.folder_to_download = folder_to_download

    def __generate_folder_name__(self):
        return generate_folder_name(self.base_url, self.date_from, self.date_to, self.period)

    def get_folder_path(self):
        return self.folder_to_download
