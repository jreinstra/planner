# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-10 06:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_degree_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='description_html',
        ),
    ]
