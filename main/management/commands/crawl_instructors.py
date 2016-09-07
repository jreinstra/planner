import os
import grequests
import time
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from django.db.models import Q
from main.models import Instructor

# Can't raise these numbers much higher without getting bad responses
MAX_INSTRUCTORS = 200
MAX_BATCH = 10
DAYS_OLD_TO_UPDATE = 14
CUTOFF_TIMESTAMP = int(time.time()) - 86400 * DAYS_OLD_TO_UPDATE

# counter from here: https://goo.gl/RdsUZH
class FeedbackCounter:
    """Object to provide a feedback callback keeping track of total calls."""
    def __init__(self):
        self.counter = 0

    def feedback(self, r, **kwargs):
        self.counter += 1
        print("{0} fetched, {1} total.".format(r.url.split("/")[-1], self.counter))
        return r


def main():
    fbc = FeedbackCounter()

    query = Instructor.objects.filter(
        Q(is_updated=False) |
        Q(updated_at__lt=CUTOFF_TIMESTAMP)
    ).order_by('updated_at')
    total = min(query.count(), MAX_INSTRUCTORS)
    instructor_list = list(query)

    print "Fetching data for %s instructors (%s total old)." % (total, query.count())
    rs = [
        grequests.get(
            "https://explorecourses.stanford.edu/instructor/" + i.sunet,
            callback=fbc.feedback
        ) for i in instructor_list[:MAX_INSTRUCTORS]
    ]
    resp = grequests.map(rs, size=MAX_BATCH)
    print "Batch requests loaded."
    for i in range(0, len(resp)):
        instructor = instructor_list[i]
        r = resp[i]
        print "Saving data for '%s'...(%s of %s)" % (instructor.sunet, i, total)
        if r is not None and r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            main_elements = soup.find(id="homeSearch").findAll("span")
            if len(main_elements) > 0 and main_elements[0].get_text() == "Personal bio":
                instructor.bio = main_elements[1].get_text()

            for element in soup.find(id="profileNavigation").findAll("span"):
                print "text:", element.get_text()
                if "I'm-not-a-bot@" not in element.get_text():
                    instructor.phone_number = element.get_text()
                else:
                    instructor.email = element.get_text().replace(
                        "I'm-not-a-bot", ""
                    ).replace(
                        "document.write('", ""
                    ).replace("');", "")

        instructor.is_updated = True
        instructor.save()
        print "...saved."
    
    
class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

if __name__ == "__main__":
    main()
