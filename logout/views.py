from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

def log_out(request):
	logout(request)
	return HttpResponseRedirect("/",{'username':"abcd"})
# Create your views here.
