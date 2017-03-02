from django.conf.urls import url
from django.views.generic import TemplateView
from . import views #, myhomeinstallation

urlpatterns = [
    # ex: /
    #url(r'^$', views.performance_report, name='home'),

    #url(r'^solarsys/(?P<installation_key>[A-Za-z0-9]+)?(?P<date>\d{2}-\d{2}-\d{4})$', views.installation_key_data, name='installation_key_data'),

    url(r'^solarsys/api/liveDC/(?P<ik>[A-Za-z0-9-]+)/(?P<today>\d{2}-\d{2}-\d{4})$', views.livedc_post, name='api_liveDC'),
    url(r'^installationkey/(?P<ik>[A-Za-z0-9-]+)$', views.installation_key_data, name='installation_key_data'),
    # ex: /reference - reference data for the day
    url(r'^reference/(?P<lat>\d+(?:\.\d+)?)/(?P<lon>\d+(?:\.\d+)?)/(?P<sc>\d+(?:\.\d+)?)/$', views.reference_data, name='reference_data'),

    # ex: /live - live data for the day
    #url(r'^live$', views.live_data, name='live_data'),
    # ex: /performance - performance measurement so far
    #url(r'^performance/$', views.performance_report, name='performance_report'),

]
