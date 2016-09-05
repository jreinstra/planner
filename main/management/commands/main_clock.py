import time
import threading

from apscheduler.schedulers.background import BackgroundScheduler
import logging
logging.basicConfig()

from . import (
    crawl_aggregate,
    crawl_courses,
    crawl_depts,
    crawl_instructors,
    crawl_reviews
)

scheduler = BackgroundScheduler()

# Tri-hourly jobs
scheduler.add_job(crawl_aggregate.main, 'interval', hours=3)
scheduler.add_job(crawl_courses.main, 'interval', hours=3)
scheduler.add_job(crawl_instructors.main, 'interval', hours=3)

# Daily jobs
scheduler.add_job(crawl_depts.main, 'interval', hours=24)
scheduler.add_job(crawl_reviews.main, 'interval', hours=24)
scheduler.start()

try:
    # keeps the main thread alive
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary but should be done if possible
    scheduler.shutdown()