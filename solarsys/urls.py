from django.conf.urls import url
#from django.views.generic.base import RedirectView
from . import views #, dailyReport

urlpatterns = [
    # ex: /
    # API URLs
    url(r'^solarsys/api/performance/', views.get_performance, name='get_performance'),

    url(r'^solarsys/api/livedc/', views.post_livedc, name='post_livedc'),
    url(r'^solarsys/api/simlivedc/', views.sim_livedc, name='sim_livedc'),
    url(r'^solarsys/api/getlivedc/', views.get_livedc, name='get_livedc'),

    url(r'^solarsys/api/postinstallationkey/', views.post_installationkey, name='post_installationkey'),
    url(r'^solarsys/api/get_nearbyinstallationkey/', views.get_nearbyinstallationkey, name='get_nearbyinstallationkey'),

    url(r'^solarsys/api/postreference/', views.post_reference, name='post_reference'),
    url(r'^solarsys/api/getreference/', views.get_reference, name='get_reference'),

   # url(r'^$', RedirectView.as_view(pattern_name='get_performance', permanent=False)),
   # url(r'^.*$', RedirectView.as_view(pattern_name='get_performance', permanent=False)),

]
