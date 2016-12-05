from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from submitprob.models import Problem
from submitprob.models import Problem
import os

# Create your views here.

def index(request,username=""):
	l=Problem.objects.all()
	return render(request,'practice/index.html',{'username': username,'problems':l})
def loadproblem(request,title,username=""):
	ob=Problem.objects.all().filter(problem_name=title)
	try:
		BASE_DIR = os.path.dirname(os.path.dirname(__file__))
		file1=open(BASE_DIR + '/Questions/'+str(ob[0].problem_id)+'/'+title+'.txt','r')
	except:
		return HttpResponse('No such question exists')
	val=file1.read()
	file1.close()
	return render(request, 'submitprob/success.html',{'username': username,'problem':ob[0],'value':val })
