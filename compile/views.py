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
# Create your views here.


def submit(request):
	return render(request, 'compile/submit.html')


def submitted(request):
	username=request.POST.get('user_name',None)
	name=request.POST.get('prob_name',None)
	ob=Problem.objects.all().filter(problem_name=name)[0]
	ob.submissions+=1
	ob.save()
	path = "compile/files/"
	complete_path = "Submissions/" + str(ob.problem_id) + "/" + username + '/'
	language=request.POST.get('language',None)
	if request.POST.get('code',None)!="":
		value=request.POST.get('code',None)
		if language == "cpp":
			try:
				file1=open(complete_path + "code" + str(ob.submissions) + ".cpp","w")
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id)+ "/" + username, shell=True)
				file1 = open(complete_path + "code" + str(ob.submissions) + ".cpp", "w")
			file1.write(value)
			file1.close()
			try:
				subprocess.call("g++ "+complete_path + "code" + str(ob.submissions) + ".cpp -o compile/files/code 2> compile/files/code.txt", shell=True)

			except OSError as e:
				return HttpResponse("Failed")
			file1=open(path+"code.txt")
			value=file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt' , shell=True)
			if value !="":
				ob.compile_error+=1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir('Questions/'+str(ob.problem_id)+'/input'):
					count += 1
				i = 0
				while i < count:
					ret=subprocess.call('timeout 2s ./compile/files/code < Questions/'+str(ob.problem_id)+'/input/input' +
									str(i) + '.txt' + ' > compile/files/output' + str(i) + '.txt'+' 2> '+' compile/files/error'+str(i)+'.txt', shell=True)
					file1=open('compile/files/error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open('compile/files/error'+str(i)+'.txt','w')
						file1.write('TLE')
						file1.close()
					i+=1

		elif language == "c":
			try:
				file1 = open(complete_path + "code" + str(ob.submissions) + ".c", "w")
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id) + "/" + str(username), shell=True)
				file1 = open(complete_path + "code" + str(ob.submissions) + ".c", "w")
			file1.write(value)
			file1.close()
			try:
				subprocess.call("gcc "+complete_path + "code" + str(ob.submissions) + ".c -o compile/files/code 2> compile/files/code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open(path + "code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt' , shell=True)
			if value != "":
				ob.compile_error += 1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir('Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i=0
				while i<count:
					ret=subprocess.call('timeout 2s ./compile/files/code < Questions/'+str(ob.problem_id)+'/input/input' +
									str(i) + '.txt' + ' > compile/files/output' + str(i) + '.txt'+' 2> '+' compile/files/error'+str(i)+'.txt',  shell=True)
					file1=open('compile/files/error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open('compile/files/error'+str(i)+'.txt','w')
						file1.write('TLE')
						file1.close()
					i+=1

		elif language == "python":
			try:
				file1 = open(complete_path + "code" + str(ob.submissions) + ".py", "w")
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id) + "/" + str(username), shell=True)
				file1 = open(complete_path + "code" + str(ob.submissions) + ".py", "w")
			file1.write(value)
			file1.close()
			try:
				subprocess.call("python3 -m py_compile "+complete_path + "code" + str(ob.submissions) + ".py 2> compile/files/code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open(path + "code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt' , shell=True)
			if value != "":
				ob.compile_error += 1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir('Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i=0
				while i<count:
					ret=subprocess.call('timeout 10s python3 '+complete_path + "code" + str(ob.submissions) + '.py < Questions/'+str(ob.problem_id)+'/input/input' +str(i) + '.txt' + ' > compile/files/output' + str(i) + '.txt'+' 2> '+' compile/files/error'+str(i)+'.txt', shell=True)
					file1=open('compile/files/error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open('compile/files/error'+str(i)+'.txt','w')
						file1.write('TLE')
						file1.close()
					i+=1
		elif language == "java":
			x=value.split(" ")
			for j in range(len(x)):
				if x[j] == "class":
					break
			y=" ".join(x)

			try:
				file1 = open(complete_path + x[j+1]+".java", "w")
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id) + "/" + str(username), shell=True)
				file1 = open(complete_path + x[j + 1] + ".java", "w")
			file1.write(y)
			file1.close()
			try:
				subprocess.call("javac "+complete_path + x[j + 1] + ".java 2> compile/files/code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open(path + "code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt' , shell=True)
			if value != "":
				ob.compile_error += 1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir('Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i=0
				while i<count:
					subprocess.call('timeout 4s java -cp ' + complete_path + x[j+1]+' < Questions/'+str(ob.problem_id)+'/input/input' +str(i) + '.txt' + ' > compile/files/output' + str(i) + '.txt'+' 2> '+' compile/files/error'+str(i)+'.txt', shell=True)
					file1=open('compile/files/error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open('compile/files/error'+str(i)+'.txt','w')
						file1.write('TLE')
						file1.close()
					i+=1


	elif request.FILES.get('file')!=None:
		file2=request.FILES['file']
		if language == "cpp":
			try:
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".cpp", ContentFile(file2.read()))
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id) + "/" + str(username), shell=True)
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".cpp", ContentFile(file2.read()))

			try:
				subprocess.call("g++ " + complete_path + "code" + str(ob.submissions) + ".cpp -o compile/files/code 2> compile/files/code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1=open("compile/files/code.txt")
			value=file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt' , shell=True)
			if value !="":
				ob.compile_error+=1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir('Questions/'+str(ob.problem_id)+'/input'):
					count += 1
				i = 0
				while i < count:
					ret=subprocess.call('timeout 2s ./compile/files/code < Questions/'+str(ob.problem_id)+'/input/input' +
									str(i) + '.txt' + ' > compile/files/output' + str(i) + '.txt'+' 2> '+' compile/files/error'+str(i)+'.txt', shell=True)
					file1=open('compile/files/error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open('compile/files/error'+str(i)+'.txt','w')
						file1.write('TLE')
						file1.close()
					i+=1



		elif language == "c":
			try:
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".c",
											 ContentFile(file2.read()))
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id) + "/" + str(username), shell=True)
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".c",
											 ContentFile(file2.read()))

			try:
				subprocess.call("gcc " + complete_path + "code" + str(ob.submissions) + ".c -o compile/files/code 2> compile/files/code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open("compile/files/code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt' , shell=True)
			if value != "":
				ob.compile_error += 1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir('Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i=0
				while i<count:
					ret=subprocess.call('timeout 2s ./compile/files/code < Questions/'+str(ob.problem_id)+'/input/input' +
									str(i) + '.txt' + ' > compile/files/output' + str(i) + '.txt'+' 2> '+' compile/files/error'+str(i)+'.txt',  shell=True)
					file1=open('compile/files/error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open('compile/files/error'+str(i)+'.txt','w')
						file1.write('TLE')
						file1.close()
					i+=1

		elif language == "python":
			try:
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".py",
											 ContentFile(file2.read()))
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id) + "/" + str(username), shell=True)
				path1 = default_storage.save(complete_path + "code" + str(ob.submissions) + ".py",
											 ContentFile(file2.read()))

			try:
				subprocess.call("python3 -m py_compile " + complete_path + "code" + str(ob.submissions) + ".py 2> compile/files/code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open("compile/files/code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt' , shell=True)
			if value != "":
				ob.compile_error += 1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir(path + 'input/'):
					count += 1
				i=0
				while i<count:
					subprocess.call('timeout 10s python3 ' + complete_path + "code" + str(ob.submissions) + '.py < Questions/'+str(ob.problem_id)+'/input/input' +str(i) + '.txt' + ' > compile/files/output' + str(i) + '.txt'+' 2> '+' compile/files/error'+str(i)+'.txt', shell=True)
					file1=open('compile/files/error'+str(i)+'.txt','r')
					v=file1.read()
					file1.close()
					if ret==124 and v=='':
						file1=open('compile/files/error'+str(i)+'.txt','w')
						file1.write('TLE')
						file1.close()
					i+=1
		elif language == "java":
			path1 = default_storage.save('compile/files/temp.txt', ContentFile(file2.read()))
			file1=open('compile/files/temp.txt')
			x=file1.read().split(" ")
			file1.close();
			subprocess.call('rm compile/files/temp.txt' , shell=True)
			for j in range(len(x)):
				if x[j] == "class":
					break;
			" ".join(y)
			try:
				file1 = open(complete_path + x[j + 1] + ".java", "w")
			except:
				subprocess.call('mkdir Submissions/' + str(ob.problem_id) + "/" + str(username), shell=True)
				file1 = open(complete_path + x[j + 1] + ".java", "w")
			file1.write(y)
			file1.close()
			try:
				subprocess.call("javac " + complete_path + x[j + 1] + ".java 2> compile/files/code.txt", shell=True)
			except OSError as e:
				return HttpResponse("Failed")
			file1 = open(path + "code.txt")
			value = file1.read()
			file1.close()
			subprocess.call('rm ' + path + 'code.txt', shell=True)
			if value != "":
				ob.compile_error += 1
				ob.save()
			elif value == "":
				value = "compiled"
				count = 0
				for i in os.listdir('Questions/' + str(ob.problem_id) + '/input'):
					count += 1
				i = 0
				while i < count:
					subprocess.call('timeout 4s java -cp ' + complete_path + x[j + 1] + ' < Questions/' + str(
						ob.problem_id) + '/input/input' + str(i) + '.txt' + ' > compile/files/output' + str(
						i) + '.txt' + ' 2> ' + ' compile/files/error' + str(i) + '.txt', shell=True)
					file1 = open('compile/files/error' + str(i) + '.txt', 'r')
					v = file1.read()
					file1.close()
					if ret == 124 and v == '':
						file1 = open('compile/files/error' + str(i) + '.txt', 'w')
						file1.write('TLE')
						file1.close()
					i += 1
	else:
		messages.error(request, 'Please enter your code or select a file')
		return HttpResponseRedirect('/practice/'+name+'/')

	subprocess.call('rm compile/files/code' , shell=True)

	if value == "compiled":
		value = "Submitted Successfully<br>"
		i=0
		c=0

		while i<count:
			fileError = open("compile/files/error" + str(i) + ".txt")
			valError = fileError.read()
			if valError == '':
				file1 = open("compile/files/output" + str(i) + ".txt")
				file2 = open("Questions/"+str(ob.problem_id)+"/output/output" + str(i) + ".txt")
				value1 = file1.read()
				value2 = file2.read()
				file1.close()
				val1=[s.strip() for s in value1.splitlines()]
				val2=[s.strip() for s in value2.splitlines()]
				#subprocess.call('rm compile/files/output' + str(i) + '.txt' , shell=True)
				file2.close()
				if val1 != val2:
					value = value + "wrong answer in test case " + str(i) + "<br>"
				else:
					c+=1
					value = value + "correct answer in test case " + str(i) + "<br>"
			elif valError == "TLE":
				value = value + "time limit exceeded in test case " + str(i) + "<br>"
			else:
				value = value + " segmentation fault in test case " + str(i) + "<br>"
			subprocess.call('rm compile/files/output' + str(i) + '.txt' , shell=True)
			subprocess.call('rm compile/files/error' + str(i) + '.txt' , shell=True)
			i += 1

		if(c==count):
			ob.correct+=1
			ob.save()



	return HttpResponse(value)
