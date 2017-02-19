from datetime import datetime, timedelta, date


def date_today():
    return datetime.now().date()


def date_weeks_ago(num_weeks, date_in=None):
    date_in = _validate_date_weeks_input(num_weeks, date_in)
    return date_in - timedelta(weeks=num_weeks)


def date_weeks_from_now(num_weeks, date_in=None):
    date_in = _validate_date_weeks_input(num_weeks, date_in)
    return date_in + timedelta(weeks=num_weeks)


def date_yahoo_finance_fmt(date_in):
    assert isinstance(date_in, date), 'Input must be a date'

    return date_in.strftime('%Y-%m-%d')


def _validate_date_weeks_input(num_weeks, date_in):
    assert isinstance(num_weeks, int), 'Num weeks must be an int'

    if date_in:
        assert isinstance(date_in, date), 'Input date must be a date'
    else:
        date_in = date_today()

    return date_in
