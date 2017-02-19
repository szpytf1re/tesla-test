from django.forms.models import ModelForm

from core_app.models.returns import TeslaReturn


class TeslaReturnForm(ModelForm):
    def __init__(self, return_date, return_amount, *args, **kwargs):
        super(TeslaReturnForm, self).__init__(*args, **kwargs)

        self.fields['return_date'].initial = return_date
        self.fields['return_amount'].initial = return_amount

        self.fields['return_date'].disabled = True
        self.fields['return_amount'].disabled = True

    class Meta(object):
        model = TeslaReturn
        fields = ['label', 'return_date', 'return_amount']
