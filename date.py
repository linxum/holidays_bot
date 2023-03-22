import datetime


def update_date():
    dt = datetime.datetime.now()
    tomorrow = dt + datetime.timedelta(days=1)
    yesterday = dt - datetime.timedelta(days=1)
    return dt, tomorrow, yesterday
