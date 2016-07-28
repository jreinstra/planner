import os
import sys
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree

from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import School, Department, Course

def populate_departments():
    schools = get_xml("http://explorecourses.stanford.edu/?view=xml-20120105")
    for school in schools.findall("school"):
        school_name = school.get("name")
        if School.objects.filter(name=school_name).exists() is False:
            school_obj = School()
            school_obj.name = school_name
            school_obj.save()
        else:
            school_obj = School.objects.get(name=school_name)
        for department in school.findall("department"):
            dept_code = department.get("name")
            if Department.objects.filter(code=dept_code).exists() is False:
                dept_obj = Department()
                dept_obj.name = department.get("name")
                dept_obj.code = dept_code
                dept_obj.school = school_obj
                dept_obj.save()
                
def populate_courses():
    dept_codes = [dept.code for dept in Department.objects.all()]
    #print dept_codes
    courses = get_xml("http://explorecourses.stanford.edu/search?view=xml-20140630&filter-coursestatus-Active=on&page=0&catalog=&q=AA")
    # this doesn't get anything ... 
    print "length:", len(courses.get("xml").get("courses").findall("course"))
    for course in courses.findall("course"):
        print "course:", course
        print "admin:", course.findall("administrativeInformation")[0][0]
        raise Exception
                
# next: http://explorecourses.stanford.edu/search?view=xml-20140630&filter-coursestatus-Active=on&page=0&catalog=&q=AA

def get_xml(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise BadAPIError(r.text)
    # x = str(r.text.encode("utf-8"))
    return ElementTree.fromstring(str(r.text.encode("utf-8")))
    
class BadAPIError(Exception):
    pass

#populate_departments()
populate_courses()