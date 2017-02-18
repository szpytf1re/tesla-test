from django.db.models.base import Model
from django.db.models.fields import DateField, CharField, DecimalField, DateTimeField


class TeslaReturn(Model):
    label = CharField(max_length=50)
    return_date = DateField()
    return_amount = DecimalField(max_digits=8, decimal_places=2)
    created_date = DateTimeField(auto_now_add=True)
