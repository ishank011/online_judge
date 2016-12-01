from django.db import models
from django.db.models.signals import post_save
from django import forms

# Create your models here.


class Problem(models.Model):
    # other fields here

    # fields in form
    problem_name = models.CharField(max_length=200)
    problem_id = models.AutoField(primary_key=True)
    submissions = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    wrong_answer = models.PositiveIntegerField(default=0)
    compile_error = models.PositiveIntegerField(default=0)
    runtime_error = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=100)

