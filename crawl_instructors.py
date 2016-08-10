import os
import requests
from bs4 import BeautifulSoup

from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import Instructor

query = Instructor.objects.filter(is_updated=False)
total = query.count()
i = 0
print "Fetching data for %s instructors." % total
for instructor in query:
    sunet = instructor.sunet
    print "Loading data for '%s'...(%s of %s)" % (sunet, i, total)
    r = requests.get("https://explorecourses.stanford.edu/instructor/" + sunet)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')

        main_elements = soup.find(id="homeSearch").findAll("span")
        if main_elements[0].get_text() == "Personal bio":
            instructor.bio = main_elements[1].get_text()

        for element in soup.find(id="profileNavigation").findAll("span"):
            if "I'm-not-a-bot@stanforddocument.write(" not in element.get_text():
                instructor.phone_number = element.get_text()
        
    instructor.is_updated = True
    instructor.save()
    i += 1