from django.conf.urls import url
from . import views

app_name = "signup"
urlpatterns = [
    url(r'^$', views.form, name='form'),
    url(r'^successful_sign_up/$', views.signup_done, name='signup_done'),
]