from urllib import urlencode

from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import TemplateView
from yahoo_finance import YQLResponseMalformedError, YQLQueryError

from core_app.forms.filter_forms import TeslaReturnFilterForm
from core_app.forms.model_forms import TeslaReturnForm


RETURN_SAVE_MSG = 'Extreme returns saved'
SOURCE_ERROR_MSG = 'Unable to reach Yahoo! Finance'


class TeslaHomeView(TemplateView):
    template_name = 'tesla/tesla_home.html'
    form = None

    def get(self, request, *args, **kwargs):
        self.form = TeslaReturnFilterForm(request.GET or None)

        if self.form.is_valid():
            redirect_url = '%s?%s' % (reverse('tesla_returns'), urlencode(self.form.get_purchase_params()))
            return HttpResponseRedirect(redirect_url)

        return super(TeslaHomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeslaHomeView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


class TeslaReturnsView(TemplateView):
    template_name = 'tesla/tesla_returns.html'

    def get_context_data(self, **kwargs):
        context = super(TeslaReturnsView, self).get_context_data(**kwargs)

        filter_form = TeslaReturnFilterForm(self.request.GET or None)

        try:
            # Extract returns data based on form filters
            returns_data = filter_form.filter()
            max_return_amount, max_return_date = filter_form.max_return
            min_return_amount, min_return_date = filter_form.min_return
        except (YQLResponseMalformedError, YQLQueryError):
            returns_data = list()

        context['filter_form'] = filter_form
        context['returns_data'] = returns_data

        if returns_data:
            context['max_return_form'] = TeslaReturnForm(max_return_date, max_return_amount, self.request.POST or None)
            context['min_return_form'] = TeslaReturnForm(min_return_date, min_return_amount, self.request.POST or None)
        else:
            context['error'] = SOURCE_ERROR_MSG

        return context

    def post(self, request, *args, **kwargs):
        del request, args, kwargs

        context = self.get_context_data()

        # Save extreme returns if label provided
        if context['max_return_form'].is_valid() and context['min_return_form'].is_valid():
            context['max_return_form'].save()
            context['min_return_form'].save()
            context['save_msg'] = RETURN_SAVE_MSG

        return self.render_to_response(context)
