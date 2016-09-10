import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from main.models import Department, Degree

BASE_URL = "http://exploredegrees.stanford.edu/"

def main():
    print "Crawling departments..."
    r = requests.get(BASE_URL)

    soup = BeautifulSoup(r.text, 'html.parser')

    for item in soup.findAll("a"):
        link = item.get("href")
        if link[0] == "/":
            full_url = BASE_URL + link[1:]
            print "\t\tTrying %s..." % link
            r = requests.get(full_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            course_block = soup.find(class_="courseblocktitle")
            if course_block is not None:
                try:
                    code = course_block.strong.text.replace(u'\xa0', " ").split("  ")[0].split(" ")[0]
                except AttributeError:
                    code = None
                    
                if code is not None:
                    dept = Department.objects.get(code=code)

                    print "Updating %s..." % dept.name
                    dept.description_html = str(soup.find(id="textcontainer"))
                    dept.save()

                    degree_types = []
                    if soup.find(id="bachelorstextcontainer") is not None or \
                       soup.find(id="bachelortextcontainer") is not None:
                        degree_types.append(1)

                    if soup.find(id="minortextcontainer") is not None:
                        degree_types.append(2)

                    if soup.find(id="coterminalmasterstextcontainer") is not None:
                        degree_types.append(3)

                    for degree_type in degree_types:
                        if Degree.objects.filter(department=dept, degree_type=degree_type).exists() is False:
                            degree = Degree(department=dept, degree_type=degree_type)
                            degree.save()

                    print "done"

                
class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

if __name__ == "__main__":
    main()
