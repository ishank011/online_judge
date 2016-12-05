from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import os,sys
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from django.conf import settings
import subprocess
from submitprob.models import Problem
from threading import Thread
import json
from django.views.decorators.csrf import csrf_exempt
import requests

def submit(request):
	return render(request, 'compile/submit.html')

def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)  
    return d

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@csrf_exempt
def getval(request):
	if request.is_ajax():
		problem_name=request.body.decode("utf-8").split('=')[1]
		ob=Problem.objects.all().filter(problem_name=problem_name)[0]
		username=request.user.username
		complete_path=BASE_DIR +"/Submissions/" + str(ob.problem_id) + "/" + username + '/'+str(ob.submissions)+'/'
		dicti={}
		count=0
		for i in os.listdir(BASE_DIR +'/Questions/' + str(ob.problem_id) + '/input'):
			count += 1
		i=0
		while i<count:
			file1=open(complete_path+"final" + str(i) + ".txt")
			val=file1.read()
			if val=='':
				dicti[str(i)]="Running"
				continue
			dicti[str(i)]=val
			file1.close()
			i+=1
		return HttpResponse(json.dumps({'dicti':dicti,'problem_name':problem_name}),content_type = 'application/javascript; charset=utf8')



def worker(username,name,language,value):
	ob=Problem.objects.all().filter(problem_name=name)[0]
	
	path = BASE_DIR +"/compile/files/"
	complete_path = BASE_DIR +"/Submissions/" + str(ob.problem_id) + "/" + username + '/'+str(ob.submissions)+'/'
	if language == "cpp":
			try:
				subprocess.call("g++ "+complete_path + "code" + str(ob.submissions) + ".cpp -o "+ complete_path + "code 2> "+ complete_path+"code.txt", shell=True)

			except OSError as e:
				return HttpResponse("Failed")
			file1=open(complete_path+"code.txt")
			value=file1.read()
			file1.close()
			subprocess.call('rm ' + complete_path + 'code.txt' , shell=True)
			if value !="":
				print(1)
				ob.compile_error+=1
				ob.save()
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input'):
					count += 1
				i=0
				while i < count:
					file1=open(complete_path+"final" + str(i) + ".txt","w")
					file1.write("Compilation Error\n")
					i += 1
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input'):
					count += 1
				i = 0
				while i < count:
					ret=subprocess.call('timeout 2s '+complete_path+'code < '+BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input/input' + str(i) + '.txt' + ' > '+complete_path+'output' + str(i) + '.txt'+' 2> '+ complete_path+'error'+str(i)+'.txt', shell=True)
					file1=open(complete_path+'error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open(complete_path+'error'+str(i)+'.txt',"w")
						file1.write('TLE')
						file1.close()
					fileError = open(complete_path+"error" + str(i) + ".txt")
					valError = fileError.read()
					if valError == '':
						file1 = open(complete_path+"output" + str(i) + ".txt")
						file2 = open(BASE_DIR +"/Questions/"+str(ob.problem_id)+"/output/output" + str(i) + ".txt")
						value1 = file1.read()
						value2 = file2.read()
						file1.close()
						val1=[s.strip() for s in value1.splitlines()]
						val2=[s.strip() for s in value2.splitlines()]
						subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file2.close()
						if val1 != val2:
							file1.write("wrong answer in test case " + str(i) +"\n")
						else:
							file1.write("correct answer in test case " + str(i) +"\n")
					elif valError == "TLE":
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Time limit exceeded in test case " + str(i) +"\n")
					else:
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Segmentation fault in test case " + str(i) +"\n")
				#subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
					subprocess.call('rm '+complete_path+'error' + str(i) + '.txt' , shell=True)
					i += 1
					file1.close()
	elif language == "c":
			try:
				subprocess.call("gcc "+complete_path + "code" + str(ob.submissions) + ".c -o "+ complete_path + "code 2> "+ complete_path+"code.txt", shell=True)

			except OSError as e:
				return HttpResponse("Failed")
			file1 = open(complete_path+"code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + complete_path + 'code.txt' , shell=True)
			if value !="":
				ob.compile_error+=1
				ob.save()
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input'):
					count += 1
				i=0
				while i < count:
					file1=open(complete_path+"final" + str(i) + ".txt","w")
					file1.write("Compilation Error\n")
					i += 1
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i=0
				while i<count:
					ret=subprocess.call('timeout 2s '+complete_path+'code < '+BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input/input' + str(i) + '.txt' + ' > '+complete_path+'output' + str(i) + '.txt'+' 2> '+ complete_path+'error'+str(i)+'.txt', shell=True)
					file1=open(complete_path+'error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open(complete_path+'error'+str(i)+'.txt',"w")
						file1.write('TLE')
						file1.close()
					fileError = open(complete_path+"error" + str(i) + ".txt")
					valError = fileError.read()
					if valError == '':
						file1 = open(complete_path+"output" + str(i) + ".txt")
						file2 = open(BASE_DIR +"/Questions/"+str(ob.problem_id)+"/output/output" + str(i) + ".txt")
						value1 = file1.read()
						value2 = file2.read()
						file1.close()
						val1=[s.strip() for s in value1.splitlines()]
						val2=[s.strip() for s in value2.splitlines()]
						subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file2.close()
						if val1 != val2:
							file1.write("wrong answer in test case " + str(i) +"\n")
						else:
							file1.write("correct answer in test case " + str(i) +"\n")
					elif valError == "TLE":
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Time limit exceeded in test case " + str(i) +"\n")
					
					else:
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Segmentation fault in test case " + str(i) +"\n")
				#subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
					subprocess.call('rm '+complete_path+'error' + str(i) + '.txt' , shell=True)
					i += 1
					file1.close()
	elif language == "python":
			try:
				subprocess.call("python3 -m py_compile "+complete_path + "code" + str(ob.submissions) + ".py 2> "+ complete_path+"code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open(complete_path+"code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + complete_path + 'code.txt' , shell=True)
			if value !="":
				ob.compile_error+=1
				ob.save()
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input'):
					count += 1
				i=0
				while i < count:
					file1=open(complete_path+"final" + str(i) + ".txt","w")
					file1.write("Compilation Error\n")
					i += 1
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i=0
				while i<count:
					ret=subprocess.call('timeout 10s python3 '+complete_path + "code" + str(ob.submissions) + '.py < '+BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input/input' +str(i) + '.txt' +  ' > '+complete_path+'output' + str(i) + '.txt'+' 2> '+ complete_path+'error'+str(i)+'.txt', shell=True)
					file1=open(complete_path+'error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open(complete_path+'error'+str(i)+'.txt',"w")
						file1.write('TLE')
						file1.close()
					fileError = open(complete_path+"error" + str(i) + ".txt")
					valError = fileError.read()
					if valError == '':
						file1 = open(complete_path+"output" + str(i) + ".txt")
						file2 = open(BASE_DIR +"/Questions/"+str(ob.problem_id)+"/output/output" + str(i) + ".txt")
						value1 = file1.read()
						value2 = file2.read()
						file1.close()
						val1=[s.strip() for s in value1.splitlines()]
						val2=[s.strip() for s in value2.splitlines()]
						subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file2.close()
						if val1 != val2:
							file1.write("wrong answer in test case " + str(i) +"\n")
						else:
							file1.write("correct answer in test case " + str(i) +"\n")
					elif valError == "TLE":
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Time limit exceeded in test case " + str(i) +"\n")
					else:
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Segmentation fault in test case " + str(i) +"\n")
				#subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
					subprocess.call('rm '+complete_path+'error' + str(i) + '.txt' , shell=True)
					i += 1
					file1.close()
	elif language == "java":
			x=value.split(" ")
			for j in range(len(x)):
				if x[j] == "class":
					break
			y=" ".join(x)
			try:
				subprocess.call("javac "+complete_path + x[j + 1] + ".java 2> "+complete_path+"code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open(complete_path + "code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + complete_path + 'code.txt' , shell=True)
			if value !="":
				ob.compile_error+=1
				ob.save()
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/'+str(ob.problem_id)+'/input'):
					count += 1
				i=0
				while i < count:
					file1=open(complete_path+"final" + str(i) + ".txt","w")
					file1.write("Compilation Error\n")
					i += 1
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir(BASE_DIR +'/Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i=0
				while i<count:
					ret=subprocess.call('timeout 10s python3 '+complete_path + "code" + str(ob.submissions) + '.py < '+'/Questions/'+str(ob.problem_id)+'/input/input' +str(i) + '.txt' +  ' > '+complete_path+'output' + str(i) + '.txt'+' 2> '+ complete_path+'error'+str(i)+'.txt', shell=True)
					file1=open(complete_path+'error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open(complete_path+'error'+str(i)+'.txt',"w")
						file1.write('TLE')
						file1.close()
					fileError = open(complete_path+"error" + str(i) + ".txt")
					valError = fileError.read()
					if valError == '':
						file1 = open(complete_path+"output" + str(i) + ".txt")
						file2 = open(BASE_DIR +"/Questions/"+str(ob.problem_id)+"/output/output" + str(i) + ".txt")
						value1 = file1.read()
						value2 = file2.read()
						file1.close()
						val1=[s.strip() for s in value1.splitlines()]
						val2=[s.strip() for s in value2.splitlines()]
						subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file2.close()
						if val1 != val2:
							file1.write("wrong answer in test case " + str(i) +"\n")
						else:
							file1.write("correct answer in test case " + str(i) +"\n")
					elif valError == "TLE":
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Time limit exceeded in test case " + str(i) +"\n")

					else:
						file1=open(complete_path+"final" + str(i) + ".txt","w")
						file1.write("Segmentation fault in test case " + str(i) +"\n")
				#subprocess.call('rm '+complete_path+'output' + str(i) + '.txt' , shell=True)
					subprocess.call('rm '+complete_path+'error' + str(i) + '.txt' , shell=True)
					i += 1
					file1.close()

	subprocess.call('rm '+complete_path+'code' , shell=True)

	
	#print("1")
	#return HttpResponse(value)



def submitted(request):
	username=request.POST.get('user_name',None)
	name=request.POST.get('prob_name',None)
	language=request.POST.get('language',None)
	ob=Problem.objects.all().filter(problem_name=name)[0]
	ob.submissions+=1
	ob.save()
	path = BASE_DIR +"/compile/files/"
	complete_path = BASE_DIR +"/Submissions/" + str(ob.problem_id) + "/" + username + '/'+str(ob.submissions)+'/'
	if request.POST.get('code',None)!="":
		value=request.POST.get('code',None)
		if language == "cpp":
			try:
				file1=open(complete_path + "code" + str(ob.submissions) + ".cpp","w+")
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				file1 = open(complete_path + "code" + str(ob.submissions) + ".cpp", "w+")
			file1.write(value)
			file1.close()
			

		elif language == "c":
			try:
				file1 = open(complete_path + "code" + str(ob.submissions) + ".c", "w+")
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				file1 = open(complete_path + "code" + str(ob.submissions) + ".c", "w+")
			file1.write(value)
			file1.close()
			

		elif language == "python":
			try:
				file1 = open(complete_path + "code" + str(ob.submissions) + ".py", "w+")
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				file1 = open(complete_path + "code" + str(ob.submissions) + ".py", "w+")
			file1.write(value)
			file1.close()
			
		elif language == "java":
			x=value.split(" ")
			for j in range(len(x)):
				if x[j] == "class":
					break
			y=" ".join(x)

			try:
				file1 = open(complete_path + x[j+1]+".java", "w+")
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				file1 = open(complete_path + x[j + 1] + ".java", "w+")
			file1.write(y)
			file1.close()
		
			

	elif request.FILES.get('file')!=None:
		file2=request.FILES['file']
		if language == "cpp":
			try:
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".cpp", ContentFile(file2.read()))
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".cpp", ContentFile(file2.read()))
			file1 = open(complete_path + "code" + str(ob.submissions) + ".cpp", "r")
			value=file1.read()
			file1.close()

		elif language == "c":
			try:
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".c",
											 ContentFile(file2.read()))
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".c",
											 ContentFile(file2.read()))
			file1 = open(complete_path + "code" + str(ob.submissions) + ".c", "r")
			value=file1.read()
			file1.close()


		elif language == "python":
			try:
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".py",
											 ContentFile(file2.read()))
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".py",
											 ContentFile(file2.read()))
			file1 = open(complete_path + "code" + str(ob.submissions) + ".py", "r")
			value=file1.read()
			file1.close()


		elif language == "java":
			path1 = default_storage.save(BASE_DIR +'/compile/files/temp.txt', ContentFile(file2.read()))
			file1=open(BASE_DIR +'/compile/files/temp.txt')
			x=file1.read().split(" ")
			file1.close();
			subprocess.call('rm '+BASE_DIR +'/compile/files/temp.txt' , shell=True)
			for j in range(len(x)):
				if x[j] == "class":
					break;
			" ".join(y)
			try:
				file1 = open(complete_path + x[j + 1] + ".java", "w+")
			except:
				subprocess.call('mkdir '+BASE_DIR +'/Submissions/' + str(ob.problem_id)+ "/" + username+'/'+str(ob.submissions), shell=True)
				file1 = open(complete_path + x[j + 1] + ".java", "w+")
			file1.write(y)
			value=y
			file1.close()
			
	else:
		messages.error(request, 'Please enter your code or select a file')
		return HttpResponseRedirect('/practice/'+name+'/')
	i=0;
	count = 0
	for i in os.listdir(BASE_DIR +'/Questions/' + str(ob.problem_id) + '/input'):
		count += 1
	i=0
	value=""
	while i<count:
		file1=open(complete_path+"final" + str(i) + ".txt","w+")
		file1.write("Running on test case "+str(i)+"\n")
		file1.close()
		value+="Running on test case "+str(i)+"\n"
		i+=1
	t = Thread(target = worker, args=[username, name, language, value, ])
	t.setDaemon(True)
	t.start()
	return render(request,'compile/submitsuccess.html',{'value':value,'problem_name':name})
