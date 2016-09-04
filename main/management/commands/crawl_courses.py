import os
import sys
import grequests
import requests
from xml.etree import ElementTree

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
            else:
                dept_obj = Department.objects.get(code=dept_code)
                
            dept_obj.name = department.get("longname")
            dept_obj.code = dept_code
            dept_obj.school = school_obj
            dept_obj.save()
                
def populate_courses():
    depts = Department.objects.all()
    rs = [
        grequests.get(
            "http://explorecourses.stanford.edu/search?view=xml-20140630&filter-coursestatus-Active=on&page=0&catalog=&q=" + dept.code,
            callback=populate_course
        ) for dept in depts
    ]
    grequests.map(rs, size=10)
    
def populate_course(r, **kwargs):
    dept = Department.objects.get(code=r.url.split("=")[-1])
    print "Loading courses for:", dept.code
    courses = get_xml_r(r)

    for course in courses[2].findall("course"):
        admin = course.findall("administrativeInformation")[0]
        course_id = int(admin[0].text)
        # TODO: check if courses of different years have different IDs
        if Course.objects.filter(id=course_id).exists() is False:
            c = Course()
        else:
            c = Course.objects.get(id=course_id)

        c.id = course_id
        c.year = course[0].text
        c.title = course[3].text.split("(")[0].strip()
        c.description = course[4].text or "No description provided."
        c.general_requirements = course[5].text or ""
        c.repeatable = False if course[6].text == "false" else True
        c.grading = course[7].text
        c.min_units = int(course[8].text)
        c.max_units = int(course[9].text)
        c.department = dept
        c.save()
        for section in course[11].findall("section"):
            section_id = int(section[0].text)

            if CourseSection.objects.filter(id=section_id).exists() is False:
                se = CourseSection()
                se.id = section_id
            else:
                se = CourseSection.objects.get(id=section_id)

            se.year = section[1].text.split(" ")[0]
            se.term = section[1].text.split(" ")[1]
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
                    instructor_obj.name = (instructor[1].text or "_") + " " + (instructor[3].text or "_")
                    instructor_obj.save()
                else:
                    instructor_obj = instructor_obj[0]
                se.instructor = instructor_obj

            se.start_date = schedule[0].text or ""
            se.end_date = schedule[1].text or ""
            se.start_time = schedule[2].text or ""
            se.end_time = schedule[3].text or ""
            se.days = get_days(schedule[5].text)
            se.save()

        code_str = course[1].text + " " + course[2].text
        code = CourseCode.objects.filter(code=code_str)
        if code.exists() is False:
            code = CourseCode()
        else:
            code = code[0]
        code.code = code_str
        code.alt_code = code_str.replace(" ", "")
        code.title = course[3].text
        code.course = c
        code.save()
    print "Finished", dept.code


def get_xml(url):
    return get_xml_r(requests.get(url))

def get_xml_r(r):
    if r.status_code != 200:
        raise BadAPIError(r.text)
    # x = str(r.text.encode("utf-8"))
    return ElementTree.fromstring(str(r.text.encode("utf-8")))

def get_days(str_in):
    return " ".join(
        [
            s for s in str_in.replace(
                "\t", " "
            ).replace(
                "\n", " "
            ).split(" ") if len(s) > 0
        ]
    )

"""def get_xml_f(url):
    return ElementTree.fromstring(open("courses.xml", "r").read())

def get_xml_s(url):
    return ElementTree.fromstring(open("schools.xml", "r").read())"""
    
class BadAPIError(Exception):
    pass

print "Loading departments..."
populate_departments()
print "Loading courses..."
populate_courses()