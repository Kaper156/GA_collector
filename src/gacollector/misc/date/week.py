import datetime


def get_previous_week_range(from_date=None):
    from_date = from_date or datetime.datetime.now()
    if type(from_date) is datetime.datetime:
        from_date = from_date.date()
    d1 = from_date - datetime.timedelta(days=from_date.weekday(), weeks=1)
    d2 = d1 + datetime.timedelta(days=6)
    return d1, d2


if __name__ == '__main__':
    assert get_previous_week_range(datetime.datetime(2020, 1, 6)) == (datetime.date(2019, 12, 30),
                                                                      datetime.date(2020, 1, 5))

    assert get_previous_week_range(datetime.datetime(2020, 4, 18)) == (datetime.date(2020, 4, 6),
                                                                       datetime.date(2020, 4, 12))
