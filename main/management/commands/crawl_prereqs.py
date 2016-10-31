import time

from django.core.management.base import BaseCommand

from main.models import Course, CourseCode

def main():
    courses = Course.objects.all()
    num_total = courses.count()
    num_finished = 0
    for course in courses:
        d = course.description
        if "requisite" in d:
            tokens = [s.upper().replace(".", "").replace(",", "").replace(";", "") for s in d[d.index("requisite"):].split(" ")]
            prev_token = ""
            results = set()
            for token in tokens:
                r = CourseCode.objects.filter(alt_code=token)
                for entry in r:
                    course.prerequisites.add(r[0])

                r = CourseCode.objects.filter(code__in=[course.department.code + " " + token, prev_token + " " + token])
                for entry in r:
                    course.prerequisites.add(entry)
                prev_token = token
        if num_finished % 100 == 0:
            print "Finished %s of %s courses." % (num_finished, num_total)
        num_finished += 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

if __name__ == "__main__":
    main()
