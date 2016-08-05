import os
import sys
import requests
from xml.etree import ElementTree

from django.core.wsgi import get_wsgi_application
os.environ["DJANGO_SETTINGS_MODULE"] = "planner.settings"
application = get_wsgi_application()

from main.models import *

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
    depts = Department.objects.all()
    
    # Only load five depts for now (to save time)
    for dept in depts:
        print "Loading courses for:", dept.code
        courses = get_xml("http://explorecourses.stanford.edu/search?view=xml-20140630&filter-coursestatus-Active=on&page=0&catalog=&q=" + dept.code)
        # this doesn't get anything ... 
        #print "length:", len(courses.get("xml").get("courses").findall("course"))
        for course in courses[2].findall("course"):
            admin = course.findall("administrativeInformation")[0]
            course_id = int(admin[0].text)
            # TODO: check if courses of different years have different IDs
            if Course.objects.filter(course_id=course_id).exists() is False:
                c = Course()
                c.course_id = course_id
                c.year = course[0].text
                c.long_name = course[3].text.split("(")[0].strip()
                c.description = course[4].text or "No description provided."
                c.general_requirements = course[5].text or ""
                c.repeatable = False if course[6].text == "false" else True
                c.grading = course[7].text
                c.min_units = int(course[8].text)
                c.max_units = int(course[9].text)
                c.department = dept
                c.save()
                for section in course[11].findall("section"):
                    se = CourseSection()
                    se.term = section[1].text
                    se.section_number = int(section[6].text)
                    se.num_enrolled = int(section[8].text)
                    se.max_enrolled = int(section[9].text)
                    se.num_waitlist = int(section[10].text)
                    se.max_waitlist = int(section[11].text)
                    se.enroll_status = section[12].text
                    se.course = c

                    schedule = section[16][0]
                    if len(schedule[6]) > 0:
                        instructor = schedule[6][0]
                        instructor_obj = Instructor.objects.filter(sunet=instructor[4].text)
                        if instructor_obj.exists() is False:
                            instructor_obj = Instructor()
                            instructor_obj.sunet = instructor[4].text
                            instructor_obj.name = instructor[1].text + " " + instructor[3].text
                            instructor_obj.save()
                        else:
                            instructor_obj = instructor_obj[0]
                        se.instructor = instructor_obj
                    se.save()

                    sc = CourseSchedule()
                    sc.start_date = schedule[0].text or ""
                    sc.end_date = schedule[1].text or ""
                    sc.start_time = schedule[2].text or ""
                    sc.end_time = schedule[3].text or ""
                    sc.days = schedule[5].text
                    sc.section = se
                    sc.save()
            else:
                c = Course.objects.get(course_id=course_id)

            code_str = course[1].text + " " + course[2].text
            code = CourseCode.objects.filter(code=code_str)
            if code.exists() is False:
                code = CourseCode()
                code.code = code_str
                code.alt_code = code_str.replace(" ", "")
                code.title = course[3].text
                code.course = c
                code.save()
                
# next: http://explorecourses.stanford.edu/search?view=xml-20140630&filter-coursestatus-Active=on&page=0&catalog=&q=AA

def get_xml(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise BadAPIError(r.text)
    # x = str(r.text.encode("utf-8"))
    return ElementTree.fromstring(str(r.text.encode("utf-8")))

"""def get_xml_f(url):
    return ElementTree.fromstring(open("courses.xml", "r").read())

def get_xml_s(url):
    return ElementTree.fromstring(open("schools.xml", "r").read())"""
    
class BadAPIError(Exception):
    pass

populate_departments()
populate_courses()