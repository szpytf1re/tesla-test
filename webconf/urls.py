from django.conf.urls import url

from core_app.views.tesla_return_views import TeslaHomeView, TeslaReturnsView

urlpatterns = [
    url(r'^$', TeslaHomeView.as_view(), name='tesla_home'),
    url(r'^returns/$', TeslaReturnsView.as_view(), name='tesla_returns')
]
