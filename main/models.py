from __future__ import unicode_literals

from django.db import models

# Create your models here.

# try this: https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-base-classes
# Need: choices for some fields & 'updated_at' and 'created_at'
class Commentable(models.Model):
    pass

class School(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    school = models.ForeignKey(School, related_name="departments")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name="requirements")
    eligible_classes = models.ManyToManyField('Course', related_name="requirements")
    num_units = models.IntegerField()
    num_classes = models.IntegerField()
    
class Course(Commentable):
    long_name = models.CharField(max_length=150)
    instructors = models.ManyToManyField('Instructor', related_name="courses")
    description = models.TextField()
    
class CourseCode(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, related_name="codes")

class Instructor(models.Model):
    sunet = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    photo_url = models.URLField(blank=True)
    phone_number = models.IntegerField(blank=True)
    email = models.CharField(max_length=40, blank=True)

class Student(models.Model):
    # needed? - could just use User
    pass

class Review(Commentable):
    author = models.ForeignKey(Student, related_name="reviews")
    
    rating = models.IntegerField()
    grade = models.CharField(max_length=2) # add choices here
    text = models.TextField()
    
    helpful_votes = models.ManyToManyField(Student, related_name="liked_reviews")
    unhelpful_votes = models.ManyToManyField(Student, related_name="+")

class Comment(Commentable):
    author = models.ForeignKey(Student, related_name="comments")
    reply_to = models.ForeignKey(Commentable, related_name="comments")
    
    text = models.CharField(max_length=250)
    likes = models.ManyToManyField(Student, related_name="liked_comments")