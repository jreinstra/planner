from __future__ import unicode_literals

import time

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from jsonfield import JSONField

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, related_name="student")
    sunet = models.CharField(max_length=10, null=True, blank=True)

# TODO: choices for some fields & 'updated_at' and 'created_at'
class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments")
    
    # generic 'reply_to' field
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comments = GenericRelation('self')
    
    text = models.CharField(max_length=250)
    
    upvotes = models.ManyToManyField(User, related_name="liked_comments")
    downvotes = models.ManyToManyField(User, related_name="+")
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(Comment, self).save(*args, **kwargs)
    
    
class School(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    school = models.ForeignKey(School, related_name="departments")
    name = models.CharField(max_length=100)
    description_html = models.TextField(default="")
    last_crawled = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name="requirements")
    eligible_classes = models.ManyToManyField('Course', related_name="requirements")
    num_units = models.IntegerField()
    num_classes = models.IntegerField()
    
class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    comments = GenericRelation(Comment)
    
    title = models.CharField(max_length=150)
    description = models.TextField()
    
    prerequisites = models.ManyToManyField('CourseCode', related_name="useful_for")
    
    general_requirements = models.CharField(max_length=100)
    repeatable = models.BooleanField()
    grading = models.CharField(max_length=40)
    min_units = models.IntegerField()
    max_units = models.IntegerField()
    
    department = models.ForeignKey(Department, related_name="courses")
    
    average_rating = models.IntegerField(default=0)
    grade_distribution = JSONField(default=None)
    median_grade = models.CharField(max_length=2, null=True, blank=True, default=None)
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def instructors(self):
        result = []
        for section in self.sections.all():
            instructor = section.instructor
            if instructor is not None and instructor not in result:
                result.append(instructor)
        return [(i.sunet, i.name) for i in result]
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(Course, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class CourseCode(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    alt_code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, related_name="codes")
    
    def __str__(self):
        return self.code
    
class CourseSection(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    
    year = models.CharField(max_length=10)
    term = models.CharField(max_length=15)
    section_number = models.IntegerField()
    component = models.CharField(max_length=4, default="")
    
    # These will need to be crawled more frequently
    num_enrolled = models.IntegerField()
    max_enrolled = models.IntegerField()
    num_waitlist = models.IntegerField()
    max_waitlist = models.IntegerField()
    enroll_status = models.CharField(max_length=32)
    
    course = models.ForeignKey(Course, related_name="sections")
    instructor = models.ForeignKey('Instructor', related_name="sections", null=True, blank=True)
    instructors = models.ManyToManyField('Instructor', related_name="sections_new")
    
    start_date = models.CharField(max_length=31)
    end_date = models.CharField(max_length=30)
    start_time = models.CharField(max_length=29)
    end_time = models.CharField(max_length=28)
    days = models.CharField(max_length=100)
    
    location = models.CharField(max_length=150)
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(CourseSection, self).save(*args, **kwargs)

class Instructor(models.Model):
    sunet = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=250, default="")
    phone_number = models.CharField(max_length=15, default="")
    bio = models.TextField(default="")
    
    is_updated = models.BooleanField(default=False)
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    comments = GenericRelation(Comment)
    
    def courses(self):
        result = []
        for section in self.sections.all():
            if section.course not in result:
                result.append(section.course)
        return [(str(c.codes.all()[0]) + ": " + c.title, c.id) for c in result]
    
    def save(self, *args, **kwargs):
        update_fields(self)
        return super(Instructor, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Review(models.Model):
    RATING_OPTIONS = (
        (1, "1 star"),
        (2, "2 stars"),
        (3, "3 stars"),
        (4, "4 stars"),
        (5, "5 stars"),
    )
    
    GRADE_OPTIONS = (
        ("A+", "A+"),
        ("A", "A"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B", "B"),
        ("B-", "B-"),
        ("C+", "C+"),
        ("C", "C"),
        ("C-", "C-"),
        ("D+", "D+"),
        ("D", "D"),
        ("D-", "D-"),
        ("F", "F"),
        ("CR", "Credit"),
        ("NC", "No credit"),
    )
    
    author = models.ForeignKey(User, related_name="reviews")
    course = models.ForeignKey(Course, related_name="reviews")
    instructor = models.ForeignKey(Instructor, related_name="reviews", null=True, blank=True)
    comments = GenericRelation(Comment)
    
    rating = models.IntegerField(choices=RATING_OPTIONS)
    grade = models.CharField(max_length=2, null=True, choices=GRADE_OPTIONS)
    text = models.TextField()
    
    upvotes = models.ManyToManyField(User, related_name="liked_reviews")
    downvotes = models.ManyToManyField(User, related_name="+")
    
    is_crawled = models.BooleanField(default=False)
    
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    
    def instructor_name(self):
        return self.instructor.name if self.instructor else None
    
    def save(self, *args, **kwargs):
        if self.is_crawled is False:
            update_fields(self)
        return super(Review, self).save(*args, **kwargs)
    
# Models for course planner
class Degree(models.Model):
    DEGREE_TYPES = (
        (1, "Bachelor's"),
        (2, "Minor"),
        (3, "Coterminal")
    )
    DEGREE_DICT = {
        1: "Bachelor's",
        2: "Minor",
        3: "Coterminal"
    }
    
    department = models.ForeignKey(Department, related_name="degrees")
    degree_type = models.IntegerField(choices=DEGREE_TYPES)
    
    name = models.CharField(max_length=150, blank=True)
    
    def _set_name(self):
        self.name = "%s in %s" % (
            self.DEGREE_DICT[self.degree_type],
            self.department.name
        )
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self._set_name()
        return super(Degree, self).save(*args, **kwargs)

class Plan(models.Model):
    student = models.ForeignKey(User, related_name="plans")
    degrees = models.ManyToManyField(Degree, related_name="plans")
    
class PlanYear(models.Model):
    student = models.ForeignKey(User, related_name="plan_years")
    plan = models.ForeignKey(Plan, related_name="years")
    year = models.CharField(max_length=10)
    
    courses = models.TextField(default="{}")
    
    summer = models.ManyToManyField(Course, blank=True, related_name="plans_summer")
    autumn = models.ManyToManyField(Course, blank=True, related_name="plans_autumn")
    winter = models.ManyToManyField(Course, blank=True, related_name="plans_winter")
    spring = models.ManyToManyField(Course, blank=True, related_name="plans_spring")
    
    summer_sections = models.ManyToManyField(CourseSection, blank=True, related_name="plans_summer")
    autumn_sections = models.ManyToManyField(CourseSection, blank=True, related_name="plans_autumn")
    winter_sections = models.ManyToManyField(CourseSection, blank=True, related_name="plans_winter")
    spring_sections = models.ManyToManyField(CourseSection, blank=True, related_name="plans_spring")
    
    
def update_fields(self):
    if not self.created_at:
        self.created_at = int(time.time())
    self.updated_at = int(time.time())