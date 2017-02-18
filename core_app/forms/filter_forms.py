from datetime import date

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms.fields import DateField, IntegerField
from django.forms.forms import Form
from yahoo_finance import Share

from base_util.date_util import date_today, date_weeks_ago, date_yahoo_finance_fmt

TSLA_START_DATE = date(2010, 6, 27)
TSLA_SYMBOL = 'TSLA'

DEFAULT_WEEKS_AGO = 4
DEFAULT_PURCHASE_QUANTITY = 1


class TeslaReturnFilterForm(Form):
    purchase_date = DateField(required=True)
    purchase_quantity = IntegerField(required=True)

    start_date = DateField(required=False)
    end_date = DateField(required=False)

    def clean(self):
        cleaned_data = super(TeslaReturnFilterForm, self).clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date < TSLA_START_DATE:
            raise ValidationError('Start date cannot be before %s.' % TSLA_START_DATE.strftime('%d/%m/%y'))

        if end_date > date_today():
            raise ValidationError('End date cannot be in the future.')

        if end_date < start_date:
            raise ValidationError('Start date must be after end date.')

        return cleaned_data

    def filter(self):
        if self.is_valid():
            start_date = self.cleaned_data['start_date']
            end_date = self.cleaned_data['end_date']
            purchase_date = self.cleaned_data['purchase_date']
            purchase_quantity = self.cleaned_data['purchase_quantity']
        else:
            start_date = date_weeks_ago(DEFAULT_WEEKS_AGO)
            end_date = date_today()
            purchase_date = start_date
            purchase_quantity = DEFAULT_PURCHASE_QUANTITY

        start_date_str = date_yahoo_finance_fmt(start_date)
        end_date_str = date_yahoo_finance_fmt(end_date)
        purchase_date_str = date_yahoo_finance_fmt(purchase_date)

        tsla = Share(TSLA_SYMBOL)
        purchase_data = tsla.get_historical(purchase_date_str, purchase_date_str)
        historical_data = tsla.get_historical(start_date_str, end_date_str)

        purchase_close = Decimal(purchase_data[0]['Close'])

        extreme_return = None
        returns_data = list()

        for data in historical_data:
            day_return = (Decimal(data['Close']) - purchase_close) * purchase_quantity
            day_data = (day_return, data['Date'])
            returns_data.append(day_data)

            if not extreme_return or day_data[0] > extreme_return[0]:
                extreme_return = day_data

        return returns_data, extreme_return
