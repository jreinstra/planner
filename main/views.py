import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.models import Token

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
        
        
class Login(APIView):    
    def get(self, request):
        print request.META
        if "HTTP_X_AXESS_TOKEN" not in request.META:
            return r_failure("Header X-Access-Token is required.")
        access_token = request.META["HTTP_X_AXESS_TOKEN"]
        try:
            user = User.objects.get(username=access_token)
        except User.DoesNotExist:
            user = User.objects.create(username=access_token)
            
        try:
            result_token = user.auth_token.key
        except Exception:
            token = Token.objects.create(user=user)
            token.save()
            result_token = token.key
        return r_success(result_token)
        
        
        
class CourseViewSet(viewsets.ModelViewSet):    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
        
        
class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
        
        
class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return self.request.user.reviews.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
    
    
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return self.request.user.comments.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
    

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