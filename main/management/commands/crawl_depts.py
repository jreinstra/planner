import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from main.models import Department, Degree

BASE_URL = "http://exploredegrees.stanford.edu/"

def main():
    r = requests.get(BASE_URL)

    soup = BeautifulSoup(r.text, 'html.parser')

    for item in soup.findAll("a"):
        link = item.get("href")
        if link[0] == "/":
            full_url = BASE_URL + link[1:]

            r = requests.get(full_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            course_block = soup.find(class_="courseblocktitle")
            if course_block is not None:
                code = course_block.strong.text.replace(u'\xa0', " ").split("  ")[0].split(" ")[0]
                dept = Department.objects.get(code=code)

                print "Updating %s..." % dept.name
                dept.description_html = str(soup.find(id="textcontainer"))
                dept.save()

                if soup.find(id="bachelorstextcontainer") is not None or \
                   soup.find(id="bachelortextcontainer") is not None:
                    degree = Degree(department=dept, degree_type=1)
                    degree.save()

                if soup.find(id="minortextcontainer") is not None:
                    degree = Degree(department=dept, degree_type=2)
                    degree.save()

                if soup.find(id="coterminalmasterstextcontainer") is not None:
                    degree = Degree(department=dept, degree_type=3)
                    degree.save()

                print "\tdone"

                
class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

if __name__ == "__main__":
    main()
