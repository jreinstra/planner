import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.utils import get_query
from main.models import CourseCode, Course, Instructor
from main.serializers import CourseSerializer, InstructorSerializer

# Create your views here.

class CourseDetailView(DetailView):
    model = Course

# adapted from: http://goo.gl/z9g4S2
class Search(APIView):
    def get(self, request):
        query_string = ''
        found_entries = None
        
        limit = request.GET.get("limit", 10)
        
        try:
            limit = int(limit)
        except ValueError:
            return r_failure("Parameter 'limit' must be an integer.")
            
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            entry_query = get_query(query_string, ['code', 'alt_code', 'title',])

            found_entries = CourseCode.objects.filter(entry_query)
            if found_entries.count() == 0:
                entry_query = get_query(query_string, ['description',])
                found_entries = [course.codes.all()[0] for course in Course.objects.filter(entry_query)]
            
            course_ids = []
            results = []
            for entry in found_entries[:limit]:
                course_id = entry.course.pk
                if entry.course.pk not in course_ids:
                    results.append({
                        "code": entry.code,
                        "title": entry.title,
                        "description": entry.course.description,
                        "course_id": course_id
                    })
                    course_ids.append(course_id)
            return r_success(results)
        else:
            return r_failure("Search parameter 'q' is required.")
        
        
class CourseDetail(APIView):
    def get(self, request, pk=None):
        courses = Course.objects.filter(pk=pk)

        if courses.count() == 1:
            return r_success(CourseSerializer(courses[0]).data)
        else:
            return r_failure("Course not found.")
        
        
class InstructorDetail(APIView):
    def get(self, request, sunet=None):
        instructors = Instructor.objects.filter(sunet=sunet)

        if instructors.count() == 1:
            return r_success(InstructorSerializer(instructors[0]).data)
        else:
            return r_failure("Instructor not found.")
    

def r_success(result):
    return Response(
        {"success":True, "result":result},
        status=status.HTTP_200_OK
    )

def r_failure(error):
    return Response(
        {"success":False, "error":str(error)},
        status=status.HTTP_400_BAD_REQUEST
    )