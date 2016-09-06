# Heroku scheduler jobs

These are the commands that should be run

## (Tri-)hourly jobs
- python manage.py crawl_aggregate
- python manage.py crawl_courses
- python manage.py crawl_instructors

## Daily jobs
- python manage.py crawl_depts
- python manage.py crawl_reviews
