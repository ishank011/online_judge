from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

def index(request,username=""):
    return render(request,'assignment/index.html',{'username': username})
