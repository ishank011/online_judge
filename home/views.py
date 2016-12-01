from django.contrib.auth.models import User
from signup.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def home(request,username=""):
	user=request.user
	#ob = User.objects.all().filter(username=user.username)
	#print(username)
	ob1 = UserProfile.objects.all().filter(user_default_info_id=user.id)
	if len(ob1)!=0:
		isteacher=ob1[0].isteacher
		ista=ob1[0].ista
	else:
		ista=0
		isteacher=0
	#print(isteacher)
	#print(ista)
	return render(request,'home/home.html',{'username': username,'isteacher':isteacher,'ista':ista})


