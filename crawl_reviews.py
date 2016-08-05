import os
import json

from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import Review, CourseCode

reviews = json.loads(open("reviews.json", "r").read())

Review.objects.filter(is_crawled=True).delete()
for review in reviews:
    code = review["course"].replace(" ", "")
    course_query = CourseCode.objects.filter(code=code)
    if course_query.exists():
        r = Review()
        r.reply_to = course_query[0].course
        r.rating = review["rating"]
        r.grade = review["grade"]
        r.text = review["text"]
        r.is_crawled = True
        r.created_at = 0
        r.updated_at = 0
        r.save()
        print "Review added to", code