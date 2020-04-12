from enum import Enum


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        raise Exception()

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        raise Exception()

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        raise Exception()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        raise Exception()


class PeriodEnum(Enum):
    DAY = 1
    WEEK = 7
    MONTH = 31


class LevelWorkEnum(OrderedEnum):
    SEND_TO_GOOGLE_SHEETS = 1
    COLLECT_RESULT = 2
    DOWNLOAD_GENERATED_URLS = 3
    GENERATE_URLS = 4


class CsvOutOpEnum(Enum):
    OVERALL = 1
    SUMMARIZE_PERIOD = 2
