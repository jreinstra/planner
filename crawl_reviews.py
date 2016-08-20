import os
import json
import time
import datetime

from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from django.contrib.auth.models import User
from main.models import Review, CourseCode

try:
    DEFAULT_USER = User.objects.get(username="anon")
except User.DoesNotExist:
    DEFAULT_USER = User.objects.create_user(username="anon")


def str_to_timestamp(date_str):
    return int(
        time.mktime(
            datetime.datetime.strptime(
                date_str, "%Y-%m-%dT%H:%M:%S.%f"
            ).timetuple()
        )
    )


reviews = json.loads(open("reviews.json", "r").read())

Review.objects.filter(is_crawled=True).delete()
total_added = 0
for review in reviews:
    code = review["course"]
    course_query = CourseCode.objects.filter(code=code)
    if course_query.exists():
        r = Review()
        r.course = course_query[0].course
        r.rating = review["rating"]
        r.grade = review["grade"]
        r.text = review["text"]
        r.is_crawled = True
        r.created_at = str_to_timestamp(review["created_at"])
        r.updated_at = str_to_timestamp(review["updated_at"])
        r.author = DEFAULT_USER
        r.save()
        total_added += 1
        if total_added % 50 == 0:
            print "Added %s reviews" % total_added