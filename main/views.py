import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.utils import get_query
from main.models import CourseCode, Course

# Create your views here.

class CourseDetailView(DetailView):
    model = Course

# adapted from: http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
class Search(APIView):
    def get(self, request):
        query_string = ''
        found_entries = None
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            entry_query = get_query(query_string, ['code', 'title',])

            found_entries = CourseCode.objects.filter(entry_query)
            if found_entries.count() == 0:
                entry_query = get_query(query_string, ['description',])
                found_entries = [course.codes.all()[0] for course in Course.objects.filter(entry_query)]
            results = []
            for entry in found_entries:
                results.append({
                    "code": entry.code,
                    "title": entry.title,
                    "description": entry.course.description,
                    "course_id": entry.course.pk
                })
            return r_success(results)
        else:
            return r_failure("Search parameter 'q' is required.")
    

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