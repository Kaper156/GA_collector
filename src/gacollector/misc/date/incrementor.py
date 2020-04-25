import calendar
import datetime

from gacollector.config.enums import PeriodEnum


class DateIncrementer:
    @classmethod
    def select_incrementer(cls, period):
        if period == PeriodEnum.DAY:
            return cls.add_day
        elif period == PeriodEnum.WEEK:
            return cls.add_week
        elif period == PeriodEnum.MONTH:
            return cls.add_month
        raise TypeError('Period doesn\'t provided! (%s)' % period)

    @classmethod
    def add_month(cls, date1):
        day = calendar.monthrange(date1.year, date1.month)[1]
        return datetime.datetime(date1.year, date1.month, day=day)

    @classmethod
    def add_week(cls, date1):
        return date1 + datetime.timedelta(days=6)

    @classmethod
    def add_day(cls, date1):
        return date1

    @classmethod
    def range_generator(cls, d_from, d_to, period):
        cur_date_1 = d_from
        cur_date_2 = None
        incrementor = cls.select_incrementer(period)
        while True:
            cur_date_2 = incrementor(cur_date_1)
            if cur_date_2 >= d_to:
                cur_date_2 = d_to
                yield cur_date_1, cur_date_2
                break

            yield cur_date_1, cur_date_2
            cur_date_1 = cur_date_2 + datetime.timedelta(days=1)


if __name__ == '__main__':
    d1, d2, d3 = datetime.datetime(2000, 1, 1), datetime.datetime(2000, 1, 31), datetime.datetime(2000, 6, 1)
    print("by day from 1-Jan 2000 to 31-Jan 2000")
    for date_range_day in DateIncrementer.range_generator(d1, d2, PeriodEnum.DAY):
        print(f"\tFrom {date_range_day[0]} to {date_range_day[1]}")

    print("by week from 1-Jan 2000 to 31-Jan 2000")
    for date_range_week in DateIncrementer.range_generator(d1, d2, PeriodEnum.WEEK):
        print(f"\tFrom {date_range_week[0]} to {date_range_week[1]}")

    print("by month from 1-Jan 2000 to 1-June 2000")
    for date_range_month in DateIncrementer.range_generator(d1, d3, PeriodEnum.MONTH):
        print(f"\tFrom {date_range_month[0]} to {date_range_month[1]}")
