# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-12 07:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_department_last_crawled'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.Instructor'),
        ),
    ]
