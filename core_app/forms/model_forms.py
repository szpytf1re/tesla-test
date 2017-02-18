from django.forms.models import ModelForm

from core_app.models.returns import TeslaReturn


class TeslaReturnForm(ModelForm):
    class Meta(object):
        model = TeslaReturn
        fields = ['label', 'return_date', 'return_amount']
