from django.conf.urls import url
from . import views

app_name = "logout"
urlpatterns = [
    url(r'^$', views.log_out, name='log_out'),
]
