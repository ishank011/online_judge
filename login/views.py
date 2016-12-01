from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from signup.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
	return render(request,'login/index.html')


def login_done(request):
	username = request.POST.get("username")
	password = request.POST.get("password")
	user=authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect("/",{'username': username})
	elif len(username)==0 or len(password)==0:
		messages.error(request, 'username and password cannot be empty')
		return HttpResponseRedirect('/login/')
	else:
		messages.error(request, 'username and password do not match')
		return HttpResponseRedirect('/login/')


'''if len(ob1)==0:
	return HttpResponseRedirect(reverse('login:index'), {'error_message': "Invalid Username"})
	else:
		ob2 = ob1[0].check_password(password)
		if not ob2:
			return HttpResponseRedirect(reverse('login:index'), {'error_message': "Invalid Username"})
	context = {'username':username}
	return render(request,'login/login_done.html',context)'''

	

