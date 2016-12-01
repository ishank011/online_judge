from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from submitprob.models import Problem
import subprocess
def problem(request):
	form = UploadFileForm()
	return render(request, 'submitprob/submit_problem.html', {'form': form})

def success(request):
	problem_name=request.POST.get('title')
	ob=Problem(problem_name=problem_name)
	ob.save()
	ob=Problem.objects.all().filter(problem_name=problem_name)
	upload_file(request,ob)
	try:
		subprocess.call('tar -xf Questions/'+str(ob[0].problem_id)+'/code.tar.gz -C '+'Questions/'+str(ob[0].problem_id)+'/',shell=True)
	except:
		return HttpResponse("Format required: .tar.gz")	
	subprocess.call('rm -r Questions/'+str(ob[0].problem_id)+'/code.tar.gz',shell=True)
	loadproblem(request,ob[0].problem_name)
	
def loadproblem(request,title):
	ob=Problem.objects.all().filter(problem_name=title)
	try:
		file1=open('Questions/'+str(ob[0].problem_id)+'/'+problem_name+'.txt','r')
	except:
		return HttpResponse("No question exists")
	val=file1.read()
	file1.close()
	return render(request, 'submitprob/success.html',{'problem':ob[0],'value':val})

def handle_uploaded_file(f,ob):
	subprocess.call('mkdir Questions/'+str(ob[0].problem_id),shell=True)
	subprocess.call('mkdir Submissions/'+str(ob[0].problem_id),shell=True)
	with open('Questions/'+str(ob[0].problem_id)+'/code.tar.gz', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def upload_file(request,ob):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'],ob)
			return HttpResponseRedirect('/success/url/')
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})
