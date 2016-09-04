import os
import requests
from bs4 import BeautifulSoup

from main.models import School, Department, Degree

for school in School.objects.all():
    school_slug = school.name.replace(" ", "").replace(",", "").replace("&", "and").lower()
    school_url = "http://exploredegrees.stanford.edu/%s/" % school_slug
    
    r = requests.get(school_url)
    if r.status_code == 200:
        print "** Updating %s **" % school.name
        
        soup = BeautifulSoup(r.text, 'html.parser')
        school.description_html = str(soup.find(id="textcontainer"))
        school.save()
        
        for dept in Department.objects.filter(school=school):
            dept_slug = dept.name.replace(" ", "").replace(",", "").replace("&", "and").lower()
            dept_url = school_url + dept_slug + "/"

            r = requests.get(dept_url)
            if r.status_code == 200:
                print "Updating %s..." % dept.code
                soup = BeautifulSoup(r.text, 'html.parser')
                dept.description_html = str(soup.find(id="textcontainer"))
                
                if soup.find(id="bachelorstextcontainer") is not None:
                    degree = Degree(department=dept, degree_type=1)
                    degree.save()
                    
                if soup.find(id="minortextcontainer") is not None:
                    degree = Degree(department=dept, degree_type=2)
                    degree.save()
                    
                if soup.find(id="coterminalmasterstextcontainer") is not None:
                    degree = Degree(department=dept, degree_type=3)
                    degree.save()
            else:
                print "Skip %s... (%s)" % (dept.name, r.status_code)
                
            dept.is_updated = True
            dept.save()
    else:
        print "** Skip %s **" % school.name