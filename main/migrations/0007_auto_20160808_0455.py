# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-08 04:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_department_is_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='description',
            new_name='description_html',
        ),
        migrations.RenameField(
            model_name='school',
            old_name='description',
            new_name='description_html',
        ),
    ]