# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-25 08:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_auto_20160525_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dob',
            field=models.CharField(default=datetime.datetime(2016, 5, 25, 8, 19, 45, 916846, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
