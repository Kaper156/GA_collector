import os

from gacollector.misc.csv.csv_set import CsvSet
from gacollector.misc.date.extractor import DateExtractor
from gacollector.misc.files.helpers import duplicate_check


class CsvFileChecker:
    def __init__(self, path_to_files: str = None, force_delete=False):
        if path_to_files is None or not os.path.exists(path_to_files):
            raise Exception("Pass correct path to folder contain files")
        self.path_to_files = path_to_files
        self.files = list()
        self.force_delete = force_delete
        self.update_files()

    def update_files(self):
        self.files = os.listdir(self.path_to_files)

    def get_incomplete_urls(self, urls: list):
        result = list()

        self.update_files()
        file_dates = ([DateExtractor.file_get_date(file) for file in self.files])

        for url in urls:
            if DateExtractor.url_get_date(url) not in file_dates:
                result.append(url)
        return result

    def delete_duplicates(self):
        duplicates = list(filter(duplicate_check, self.files))
        cnt = len(duplicates)
        if cnt > 0:
            old_cur_dir = os.path.abspath(os.path.curdir)
            os.chdir(self.path_to_files)
            for duplicate in duplicates:
                path_to_duplicate = os.path.join(self.path_to_files, duplicate)
                print(f"\"{path_to_duplicate}\" is duplicate and will be removed")
                os.remove(duplicate)
            os.chdir(old_cur_dir)
        return cnt

    def get_invalid_files(self):
        invalid_files = list()
        reader = CsvSet(self.path_to_files, '', '')  # Use for only read
        header = None
        for filename, csv_rows in reader.get_csv_readers():
            header = header or csv_rows.fieldnames
            if csv_rows.fieldnames and header != csv_rows.fieldnames:
                invalid_files.append(os.path.join(self.path_to_files, filename))
        return invalid_files

    def delete_invalid_files(self):
        invalid_files = self.get_invalid_files()
        cnt = len(invalid_files)
        if len(invalid_files) < 1:
            return 0
        print("These files contain invalid headers:")
        for index, file_path in enumerate(invalid_files):
            print(f"{index}\t{file_path}")

        if self.force_delete or input("Type 'y' if you agree delete these files:").strip() == 'y':
            for file_path in invalid_files:
                os.remove(file_path)
            print("Files deleted")
            return cnt
        return 0

    def clear_folder(self):
        self.delete_invalid_files()
        self.delete_duplicates()


if __name__ == '__main__':
    print(os.path.abspath(os.path.curdir))
    c = CsvFileChecker('../../bin')
    # print(c.files)
    # c.delete_duplicates()
    # c.delete_invalid_files()
    c.clear_folder()
