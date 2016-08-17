import os
import json

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import Course, Review

total_courses = Course.objects.all().count()
num_courses_done = 0

for course in Course.objects.all():
    if course.reviews.count() == 0:
        average_rating = None
        grade_distribution = None
    else:
        average_rating = 0.0
        grade_counts = {option[0]:0 for option in Review.GRADE_OPTIONS}
        total_reviews = 0
        for review in course.reviews.all():
            average_rating += review.rating
            if review.grade in grade_counts:
                grade_counts[review.grade] += 1
            total_reviews += 1
        average_rating = int(10 * average_rating / total_reviews) / 10.0
        grade_distribution = json.dumps([(option[0], grade_counts[option[0]]) for option in Review.GRADE_OPTIONS])
        
    course.average_rating = average_rating
    course.grade_distribution = grade_distribution
    course.save()
    
    num_courses_done += 1
    if num_courses_done % 50 == 0:
        print "Updated %s of %s courses." % (num_courses_done, total_courses)