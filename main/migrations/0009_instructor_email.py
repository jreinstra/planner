# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-07 07:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20160907_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='email',
            field=models.CharField(default='', max_length=250),
        ),
    ]
