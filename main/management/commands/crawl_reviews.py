import os
import json
import time
import datetime

from django.core.management.base import BaseCommand

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


def main():
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
            r.text = review["text"].replace("<div>", "").replace("</div>", "")
            r.is_crawled = True
            r.created_at = str_to_timestamp(review["created_at"])
            r.updated_at = str_to_timestamp(review["updated_at"])
            r.author = DEFAULT_USER
            r.save()
            total_added += 1
            if total_added % 50 == 0:
                print "Added %s reviews" % total_added
                
                
class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

if __name__ == "__main__":
    main()
