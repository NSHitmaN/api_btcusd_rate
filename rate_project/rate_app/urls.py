from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^current/$', views.calc_avg, name='calc_avg'),
    url(r'^history/$', views.history, name='history'),
]

