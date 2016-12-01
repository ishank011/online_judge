from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import datetime
from .models import UserProfile
from django.template import loader
from django.contrib import messages
from django.core.mail import send_mail



# Create your views here.

def form(request):
    return render(request,'signup/form.html')


def signup_done(request):
    username=request.POST.get('username')
    first_name=request.POST.get('first_name')
    middle_name=request.POST.get('middle_name')
    last_name=request.POST.get('last_name')
    gender=request.POST.get('gender')
    dob=request.POST.get('dob')
    email=request.POST.get('email')
    contact_number=request.POST.get('contact_number')
    institute=request.POST.get('institute')
    year_joined_institute=request.POST.get('year_joined_institute')
    city=request.POST.get('city')
    country=request.POST.get('country')
    tshirt_size=request.POST.get('tshirt_size')

    if (len(username) == 0):
        messages.error(request, 'username cannot be empty')
        return HttpResponseRedirect('/signup/')


    try:
        dob_object = datetime.strptime(dob,'%d/%m/%Y')
    except:
        messages.error(request, 'Input Date Of Birth in format dd/mm/yyyy')
        return HttpResponseRedirect('/signup/')

    ob4 = User.objects.all().filter(username=username)
    if len(ob4) != 0:
        messages.error(request, 'username already exists')
        return HttpResponseRedirect('/signup/')


    ob = User(username=username,
              first_name=first_name,
              last_name=last_name,
              email=email,
              )
    ob.set_password('1234')
    ob.save()
    ob3 = User.objects.all().filter(username=username)

    ob2 = UserProfile(user_default_info=ob3[0],
                      middle_name=middle_name,
                      gender=gender,
                      dob=dob,
                      contact_number=contact_number,
                      institute=institute,
                      year_joined_institute=year_joined_institute,
                      city=city,
                      country=country,
                      tshirt_size=tshirt_size
                      )
    ob2.save()
    return HttpResponse('Signup successful and your password is 1234. Please log in to continue')
