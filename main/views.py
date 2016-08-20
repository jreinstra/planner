import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

from main.utils import get_query
from main.models import CourseCode, Course, Instructor, Review, Comment
from main.serializers import *

# Create your views here.

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
            for entry in found_entries:
                course_id = entry.course.pk
                if entry.course.pk not in course_ids:
                    results.append({
                        "code": entry.code,
                        "title": entry.title,
                        "description": entry.course.description,
                        "id": course_id
                    })
                    course_ids.append(course_id)
                    
                    if len(results) == limit:
                        break
            return r_success(results)
        else:
            return r_failure("Search parameter 'q' is required.")
        
        
class CourseViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
        
        
class InstructorViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
        
        
class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return self.request.user.reviews.all()
    
    
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return self.request.user.comments.all()
    

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