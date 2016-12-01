from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^teacher/$', views.addteacher, name='addteacher'),
    url(r'^question/$', views.addquestion, name='addquestion'),
    url(r'^ta/$', views.addta, name='addta'),
    url(r'^course/$', views.addcourse, name='addcourse'),
    url(r'^teacher/success$', views.addteacherdone, name='addteacherdone'),
    url(r'^question/success$', views.addquestiondone, name='addquestiondone'),
    url(r'^ta/success$', views.addtadone, name='addtadone'),
    url(r'^course/success$', views.addcoursedone, name='addcoursedone'),

]
