# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160802_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='general_requirements',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]