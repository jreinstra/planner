import os
import sys
from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import Course

print Course.objects.all()