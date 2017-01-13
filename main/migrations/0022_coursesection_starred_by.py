# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-13 06:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0021_coursesection_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursesection',
            name='starred_by',
            field=models.ManyToManyField(related_name='starred_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
