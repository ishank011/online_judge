from django.conf.urls import url
from . import views

app_name = "submitprob"
urlpatterns = [
    url(r'^$', views.problem, name='problem'),
    url(r'^successful/$', views.success, name='success'),
]
