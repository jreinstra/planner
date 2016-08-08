from __future__ import unicode_literals

from django.db import models

import time
# Create your models here.

# TODO: choices for some fields & 'updated_at' and 'created_at'
class Commentable(models.Model):
    pass

class School(models.Model):
    name = models.CharField(max_length=100)
    description_html = models.TextField(default="")
    
    def __str__(self):
        return self.name

class Department(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    school = models.ForeignKey(School, related_name="departments")
    name = models.CharField(max_length=100)
    description_html = models.TextField(default="")
    
    is_updated = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name="requirements")
    eligible_classes = models.ManyToManyField('Course', related_name="requirements")
    num_units = models.IntegerField()
    num_classes = models.IntegerField()
    
class Course(Commentable):
    course_id = models.IntegerField(primary_key=True)
    
    title = models.CharField(max_length=150)
    description = models.TextField()
    
    general_requirements = models.CharField(max_length=100)
    repeatable = models.BooleanField()
    grading = models.CharField(max_length=40)
    min_units = models.IntegerField()
    max_units = models.IntegerField()
    
    department = models.ForeignKey(Department, related_name="courses")
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(Course, self).save(*args, **kwargs)
    
class CourseCode(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    alt_code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, related_name="codes")
    
    def __str__(self):
        return self.code
    
class CourseSection(models.Model):
    year = models.CharField(max_length=10)
    term = models.CharField(max_length=15)
    section_number = models.IntegerField()
    
    # These will need to be crawled more frequently
    num_enrolled = models.IntegerField()
    max_enrolled = models.IntegerField()
    num_waitlist = models.IntegerField()
    max_waitlist = models.IntegerField()
    enroll_status = models.CharField(max_length=15)
    
    course = models.ForeignKey(Course, related_name="sections")
    instructor = models.ForeignKey('Instructor', related_name="sections", blank=True, null=True)
    
    start_date = models.CharField(max_length=15)
    end_date = models.CharField(max_length=15)
    start_time = models.CharField(max_length=15)
    end_time = models.CharField(max_length=15)
    days = models.CharField(max_length=100)
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(CourseSection, self).save(*args, **kwargs)

class Instructor(models.Model):
    sunet = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, default="")
    bio = models.TextField(default="")
    
    is_updated = models.BooleanField(default=False)
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(Instructor, self).save(*args, **kwargs)

class Student(models.Model):
    # needed? - could just use User
    pass

class Review(Commentable):
    author = models.ForeignKey(Student, related_name="reviews", null=True, blank=True)
    reply_to = models.ForeignKey(Course, related_name="reviews")
    
    rating = models.IntegerField()
    grade = models.CharField(max_length=2, null=True) # add choices here
    text = models.TextField()
    
    helpful_votes = models.ManyToManyField(Student, related_name="liked_reviews")
    unhelpful_votes = models.ManyToManyField(Student, related_name="+")
    
    is_crawled = models.BooleanField(default=False)
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def save(self, *args, **kwargs):
        if self.is_crawled is False:
            update_fields(self)
        return super(Review, self).save(*args, **kwargs)

class Comment(Commentable):
    author = models.ForeignKey(Student, related_name="comments")
    reply_to = models.ForeignKey(Commentable, related_name="comments")
    
    text = models.CharField(max_length=250)
    likes = models.ManyToManyField(Student, related_name="liked_comments")
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(Comment, self).save(*args, **kwargs)
    
    
def update_fields(self):
    if not self.created_at:
        self.created_at = int(time.time())
    self.updated_at = int(time.time())