import os
import sys
import requests
from bs4 import BeautifulSoup

from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import Course

print Course.objects.all()
r = requests.get("http://explorecourses.stanford.edu/?view=xml-20120105")
r = requests.get("http://explorecourses.stanford.edu/search?view=xml-20140630&filter-coursestatus-Active=on&page=0&catalog=&q=AA")
print r.text
soup = BeautifulSoup(r.text, 'html.parser')
soup.find_all('div')