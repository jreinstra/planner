from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    pass

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, related_name="requirements")
    eligible_classes = models.ManyToManyField('Class', related_name="requirements")
    num_units = models.IntegerField()
    num_classes = models.IntegerField()
    
class Class(models.Model):
    pass

class Instructor(models.Model):
    pass

class Student(models.Model):
    pass

class Review(models.Model):
    pass

class Comment(models.Model):
    pass