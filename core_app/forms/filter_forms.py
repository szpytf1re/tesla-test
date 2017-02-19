from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.forms.fields import DateField, IntegerField
from django.forms.forms import Form
from yahoo_finance import Share

from base_util.date_util import date_today, date_weeks_ago, date_yahoo_finance_fmt, date_weeks_from_now

TSLA_START_DATE = date(2010, 6, 28)
TSLA_SYMBOL = 'TSLA'

DEFAULT_WEEKS_DELTA = 4
DEFAULT_PURCHASE_QUANTITY = 1


class TeslaReturnFilterForm(Form):
    purchase_date = DateField(required=True)
    purchase_quantity = IntegerField(required=True, min_value=1)

    start_date = DateField(required=False)
    end_date = DateField(required=False)

    max_return = None
    min_return = None

    def clean(self):
        cleaned_data = super(TeslaReturnFilterForm, self).clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        purchase_date = cleaned_data.get('purchase_date')

        todays_date = date_today()

        if purchase_date <= TSLA_START_DATE:
            raise ValidationError('Purchase date cannot be before %s.' % TSLA_START_DATE.strftime('%m/%d/%y'))

        if start_date and start_date <= TSLA_START_DATE:
            raise ValidationError('Start date cannot be before %s.' % TSLA_START_DATE.strftime('%m/%d/%y'))

        if end_date and end_date > todays_date:
            raise ValidationError('End date cannot be in the future.')

        if start_date and end_date and end_date < start_date:
            raise ValidationError('Start date must be before end date.')

        if purchase_date >= todays_date:
            raise ValidationError('Purchase date must be before today.')

        if start_date and purchase_date > start_date:
            raise ValidationError('Start date must be after purchase date.')

        if end_date and purchase_date >= end_date:
            raise ValidationError('End date must be after purchase date.')

        return cleaned_data

    def filter(self):
        # Defaults
        start_date = date_weeks_ago(DEFAULT_WEEKS_DELTA)
        end_date = date_today()
        purchase_date = start_date
        purchase_quantity = DEFAULT_PURCHASE_QUANTITY

        if self.is_valid():
            purchase_date = self.cleaned_data['purchase_date']
            purchase_quantity = self.cleaned_data['purchase_quantity']

            # Both start and end date inputs provided
            if self.cleaned_data['start_date'] and self.cleaned_data['end_date']:
                start_date = self.cleaned_data['start_date']
                end_date = self.cleaned_data['end_date']

            # Only start date input provided
            elif self.cleaned_data['start_date'] and not self.cleaned_data['end_date']:
                start_date = self.cleaned_data['start_date']
                end_date = min(date_weeks_from_now(DEFAULT_WEEKS_DELTA, date_in=start_date), date_today())

            # Only end date input provided
            elif self.cleaned_data['end_date'] and not self.cleaned_data['start_date']:
                end_date = self.cleaned_data['end_date']
                start_date = max(date_weeks_ago(DEFAULT_WEEKS_DELTA, date_in=end_date), purchase_date)

        # Convert dates to yahoo finance strings
        start_date_str = date_yahoo_finance_fmt(start_date)
        end_date_str = date_yahoo_finance_fmt(end_date)
        purchase_date_str = date_yahoo_finance_fmt(purchase_date)

        # Pull down data from API
        tsla = Share(TSLA_SYMBOL)
        purchase_data = tsla.get_historical(purchase_date_str, purchase_date_str)
        historical_data = tsla.get_historical(start_date_str, end_date_str)

        # Reverse historical data so that it is ordered by date ascending
        historical_data = historical_data[::-1]

        purchase_close = Decimal(purchase_data[0]['Close'])

        returns_data = list()

        # Extract required historical data
        for data in historical_data:
            # Calculate return for given day
            day_return = (Decimal(data['Close']) - purchase_close) * purchase_quantity

            day_data = (day_return, data['Date'])
            returns_data.append(day_data)

            # Set max return
            if not self.max_return or day_data[0] > self.max_return[0]:
                self.max_return = day_data

            # Set min return
            if not self.min_return or day_data[0] < self.min_return[0]:
                self.min_return = day_data

        return returns_data

    def get_purchase_params(self):
        assert self.is_valid(), 'Form must be valid to get purchase params'
        return {
            'purchase_date': self.cleaned_data['purchase_date'],
            'purchase_quantity': self.cleaned_data['purchase_quantity']
        }
