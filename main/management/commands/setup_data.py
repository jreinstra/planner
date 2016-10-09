from crawl_aggregate import main as run_aggregate
from crawl_courses import main as run_courses
from crawl_depts import main as run_depts
from crawl_instructors import main as run_instructors
from crawl_prereqs import main as run_prereqs
from crawl_reviews import main as run_reviews

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        run_courses()
        run_instructors()
        run_depts()
        run_reviews()
        run_aggregate()
        run_prereqs()
