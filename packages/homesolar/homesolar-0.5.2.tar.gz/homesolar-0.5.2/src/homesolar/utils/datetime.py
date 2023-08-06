from datetime import datetime, timedelta
from time import time


def stringify_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_today():
    return datetime.fromtimestamp(time()).replace(hour=0, minute=0, second=0).timestamp()


def get_next_day(timestamp):
    return (datetime.utcfromtimestamp(timestamp) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_first_day_of_month(timestamp):
    return datetime.utcfromtimestamp(timestamp).replace(day=1).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_last_day_of_month(timestamp):
    next_month = datetime.utcfromtimestamp(timestamp).replace(day=28) + timedelta(days=4)
    return (next_month - timedelta(days=next_month.day)).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_first_day_of_year(timestamp):
    return datetime.utcfromtimestamp(timestamp).replace(day=1, month=1).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_last_day_of_year(timestamp):
    return datetime.utcfromtimestamp(timestamp).replace(day=31, month=12).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_date_pair(date, timescale):

    if timescale == "MONTH":
        start_time = get_first_day_of_month(date)
        stop_time = get_last_day_of_month(date)
    elif timescale == "YEAR":
        start_time = get_first_day_of_year(date)
        stop_time = get_last_day_of_year(date)
    else:
        start_time = stringify_timestamp(date)
        stop_time = get_next_day(date)

    return start_time, stop_time
