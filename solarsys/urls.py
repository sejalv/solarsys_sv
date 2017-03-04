from django.conf.urls import url
from django.views.generic import TemplateView
from . import views #, myhomeinstallation

urlpatterns = [
    # ex: /
    #url(r'^$', views.get_performance, name='home'),

    # API URLs
    url(r'^solarsys/api/performance/', views.get_performance, name='get_performance'),
    url(r'^solarsys/api/livedc/', views.post_livedc, name='post_livedc'),
    url(r'^solarsys/api/simlivedc/', views.sim_livedc, name='sim_livedc'),
    url(r'^solarsys/api/getlivedc/', views.get_livedc, name='get_livedc'),

    url(r'^solarsys/api/getinstallationkey/', views.get_installationkey, name='get_installationkey'),
    url(r'^solarsys/api/postinstallationkey/', views.post_installationkey, name='post_installationkey'),

    url(r'^solarsys/api/getreference/', views.get_reference, name='get_reference'),
    url(r'^solarsys/api/postreference/', views.post_reference, name='post_reference'),

]
