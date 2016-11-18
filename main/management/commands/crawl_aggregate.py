import os
import json

from django.core.management.base import BaseCommand

from main.models import Course, Review



def main():
    total_courses = Course.objects.all().count()
    num_courses_done = 0

    for course in Course.objects.all():
        median_grade = None
        
        if course.reviews.count() == 0:
            average_rating = 0.0
            grade_distribution = None
        else:
            average_rating = 0.0
            grade_counts = {option[0]:0 for option in Review.GRADE_OPTIONS}
            total_reviews = 0
            total_grades = 0
            for review in course.reviews.all():
                if review.rating != 0:
                    average_rating += review.rating
                    total_reviews += 1
                if review.grade in grade_counts:
                    grade_counts[review.grade] += 1
                    total_grades += 1
            
            if total_reviews > 0:
                average_rating = round(average_rating / total_reviews)
            grade_distribution = [(option[0], grade_counts[option[0]]) for option in Review.GRADE_OPTIONS]
            
            current_value = 0
            median_value = total_grades / 2
            for grade, value in grade_distribution:
                current_value += value
                if current_value > median_value:
                    median_grade = grade
                    break
                    
        course.average_rating = average_rating
        course.grade_distribution = json.dumps(grade_distribution)
        course.median_grade = median_grade
        course.save()

        num_courses_done += 1
        if num_courses_done % 50 == 0:
            print "Updated %s of %s courses." % (num_courses_done, total_courses)
        
        
class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

if __name__ == "__main__":
    main()
