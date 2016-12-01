# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-25 07:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_userprofile_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dob',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='contact_number',
            field=models.CharField(default=datetime.datetime(2016, 5, 25, 7, 21, 25, 305312, tzinfo=utc), max_length=12),
            preserve_default=False,
        ),
    ]
