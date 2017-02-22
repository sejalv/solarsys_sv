from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.performance_report, name='home'),
    # ex: /live - live data for the day
    url(r'^live$', views.live_data, name='live_data'),
    # ex: /reference - reference data for the day
    url(r'^reference$', views.reference_data, name='reference_data'),
    # ex: /performance - performance measurement so far
    url(r'^performance/$', views.performance_report, name='performance_report'),
    #url(r'^simpleemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', views.sendHTMLEmail , name = 'sendSimpleEmail')
]
