from datetime import datetime, timedelta, date


def date_today():
    return datetime.now().date()


def date_weeks_ago(num_weeks):
    assert isinstance(num_weeks, int), 'Num weeks must be an int'

    return date_today() - timedelta(weeks=num_weeks)


def date_yahoo_finance_fmt(date_in):
    assert isinstance(date_in, date), 'Input must be a date'

    return date_in.strftime('%Y-%m-%d')
