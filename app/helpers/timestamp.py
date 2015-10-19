import datetime


def dt_to_ts(dt):
    assert isinstance(dt, datetime.datetime)
    return int(round((dt - datetime.datetime(1970, 1, 1)).total_seconds()))


