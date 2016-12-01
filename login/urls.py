from django.conf.urls import url
from . import views

app_name = "login"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.login_done, name='login_done'),
]
