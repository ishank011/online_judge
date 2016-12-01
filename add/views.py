from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import datetime
from signup.models import UserProfile
from django.template import loader
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def addteacher(request,username=""):
    return render(request, 'add/addteacher.html', {'username': username})

def addta(request,username=""):
    user = request.user
    ob1 = UserProfile.objects.all().filter(user_default_info_id=user.id)
    if len(ob1) != 0:
        isteacher = ob1[0].isteacher
        ista = ob1[0].ista
    else:
        ista = 0
        isteacher = 0
    return render(request, 'add/addta.html', {'username': username,'isteacher':isteacher,'ista':ista})

def addcourse(request,username=""):
    return HttpResponse('abcd')

def addquestion(request,username=""):
    return HttpResponse('abcd')

def addteacherdone(request):
    val = request.POST.get('username')
    ob = User.objects.all().filter(username=val)
    if len(ob)==0:
        messages.error(request, 'username does not exist')
        return HttpResponseRedirect('/add/teacher')
    else:
        ob1=UserProfile.objects.all().filter(user_default_info_id=ob[0].id)
        ob1[0].isteacher=True
        ob1[0].save()
        messages.success(request, 'Teacher Added')
    return HttpResponseRedirect('/add/teacher')

def addtadone(request,username=""):
    val = request.POST.get('username')
    ob = User.objects.all().filter(username=val)
    if len(ob) == 0:
        messages.error(request, 'username does not exist')
        return HttpResponseRedirect('/add/ta')
    else:
        ob1 = UserProfile.objects.all().filter(user_default_info_id=ob[0].id)
        ob1[0].ista = True
        ob1[0].save()
        messages.success(request, 'TA Added')
    return HttpResponseRedirect('/add/ta')
def addcoursedone(request,username=""):
    return HttpResponse('abcd')

def addquestiondone(request,username=""):
    return HttpResponse('abcd')
