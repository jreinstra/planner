# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 04:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commentable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('sunet', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('photo_url', models.URLField(blank=True)),
                ('phone_number', models.IntegerField(blank=True)),
                ('email', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('num_units', models.IntegerField()),
                ('num_classes', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='main.Department')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Commentable')),
                ('text', models.CharField(max_length=250)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.Student')),
                ('likes', models.ManyToManyField(related_name='liked_comments', to='main.Student')),
            ],
            bases=('main.commentable',),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('commentable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Commentable')),
                ('long_name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('instructors', models.ManyToManyField(related_name='courses', to='main.Instructor')),
            ],
            bases=('main.commentable',),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('commentable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Commentable')),
                ('rating', models.IntegerField()),
                ('grade', models.CharField(max_length=2)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.Student')),
                ('helpful_votes', models.ManyToManyField(related_name='liked_reviews', to='main.Student')),
                ('unhelpful_votes', models.ManyToManyField(related_name='_review_unhelpful_votes_+', to='main.Student')),
            ],
            bases=('main.commentable',),
        ),
        migrations.AddField(
            model_name='department',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='main.School'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='eligible_classes',
            field=models.ManyToManyField(related_name='requirements', to='main.Course'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.Commentable'),
        ),
    ]