from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms

# Create your models here.


class UserProfile(models.Model):
    user_default_info = models.OneToOneField(User)
    # other fields here

    # fields in form
    middle_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length=50)
    institute = models.CharField(max_length=200)
    year_joined_institute = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    tshirt_size = models.CharField(max_length=3)
    contact_number = models.CharField(max_length=12)
    isteacher=models.BooleanField(default=False)
    ista=models.BooleanField(default=False)
    isstudent=models.BooleanField(default=True)

    # fields to be updated automatically after submission
    submissions = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    wrong_answer = models.PositiveIntegerField(default=0)
    compile_error = models.PositiveIntegerField(default=0)
    runtime_error = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)
    institute_rank = models.PositiveIntegerField(default=0)

class Courses(models.Model):
    course_name=models.CharField(max_length=100)
    students=models.ManyToManyField(UserProfile,related_name="students")
    tas=models.ManyToManyField(UserProfile,related_name="tas")
    teachers=models.ManyToManyField(UserProfile,related_name="teachers")