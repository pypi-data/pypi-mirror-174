import datetime


def cur_time_str():
    now = datetime.datetime.now()
    return str(now)[0:19].replace(' ', '_').replace(':', '')
