import os
import grequests
from bs4 import BeautifulSoup

from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import Instructor

# counter from here: https://goo.gl/RdsUZH
class FeedbackCounter:
    """Object to provide a feedback callback keeping track of total calls."""
    def __init__(self):
        self.counter = 0

    def feedback(self, r, **kwargs):
        self.counter += 1
        print("{0} fetched, {1} total.".format(r.url.split("/")[-1], self.counter))
        return r


fbc = FeedbackCounter()

query = Instructor.objects.filter(is_updated=False)
total = query.count()
instructor_list = list(query)

print "Fetching data for %s instructors." % total
rs = [
    grequests.get(
        "https://explorecourses.stanford.edu/instructor/" + i.sunet,
        callback=fbc.feedback
    ) for i in instructor_list
]
resp = grequests.map(rs, size=10)
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
            if "I'm-not-a-bot@" not in element.get_text():
                instructor.phone_number = element.get_text()
        
    instructor.is_updated = True
    instructor.save()