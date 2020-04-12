from gacollector.misc.folder_name import generate_folder_name
from gacollector.settings.enums import PeriodEnum


class RunnerSettings:
    def __init__(self, base_url=None, date_from=None, date_to=None, period=PeriodEnum.DAY, folder=None):
        self.base_url = base_url
        self.date_from, self.date_to = None, None
        if base_url is not None:
            # TODO
            self.date_from = ''
            self.date_to = str()
        self.period = period or PeriodEnum.DAY
        self.folder = folder or self.get_folder()

    def get_urls(self):
        if self.base_url is None:
            raise Exception("Set base url")
        # TODO
        return list()

    def get_folder(self):
        if self.folder:
            return self.folder

        self.folder = generate_folder_name(
            url=self.base_url,
            d_from=self.date_from,
            d_to=self.date_to,
            d_type=self.period
        )
        return self.folder
