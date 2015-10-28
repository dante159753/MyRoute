import datetime
import pytz


def dt_to_ts(dt):
    assert isinstance(dt, datetime.datetime)
    return int(round((dt - datetime.datetime(1970, 1, 1)).total_seconds()))


def get_formatted_time(ts):
    assert isinstance(ts, int)
    local = pytz.timezone('Asia/Chongqing')
    utc_time = datetime.datetime.utcfromtimestamp(ts)
    local_time = pytz.utc.localize(utc_time, is_dst=None).astimezone(local)
    return local_time.strftime('%Y-%m-%d')
