import json
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from main.utils import get_query
from main.models import *
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
            raise ValidationError("Parameter 'limit' must be an integer.")
            
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            
            entry_query = get_query(query_string.replace(" ", ""), ['alt_code',])
            found_entries = CourseCode.objects.filter(entry_query)
            
            if found_entries.count() == 0:
                entry_query = get_query(query_string, ['code', 'alt_code',])
                found_entries = CourseCode.objects.filter(entry_query)

                if found_entries.count() == 0:
                    entry_query = get_query(query_string, ['title'])
                    found_entries = [course.codes.all()[0] for course in Course.objects.filter(entry_query)]

                    if len(found_entries) == 0:
                        entry_query = get_query(query_string, ['description'])
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
                        "average_rating": entry.course.average_rating,
                        "min_units": entry.course.min_units,
                        "max_units": entry.course.max_units,
                        "id": course_id
                    })
                    course_ids.append(course_id)
                    
                    if len(results) == limit:
                        break
            return Response(results)
        else:
            raise ValidationError("Search parameter 'q' is required.")
        
        
class Login(APIView):    
    def post(self, request):
        if "fb_access_token" not in request.data:
            raise ValidationError("POST param 'fb_access_token' is required.")
        access_token = request.data["fb_access_token"][:30]
        
        r = requests.get("https://graph.facebook.com/me?access_token=" + request.data["fb_access_token"])
        if r.status_code != 200:
            raise ValidationError("Invalid FB access token.")
        result = r.json()
        username = result["id"]
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create(username=username)
            
        try:
            result_token = user.auth_token.key
        except Exception:
            token = Token.objects.create(user=user)
            token.save()
            result_token = token.key
        return Response(result_token)
        
        
class Vote(APIView):
    OBJ_CHOICES = {
        "review": (Review, ReviewSerializer),
        "comment":(Comment, CommentSerializer)
    }
    
    def post(self, request):
        if "obj" not in request.data or request.data["obj"] not in self.OBJ_CHOICES:
            raise ValidationError(
                "'obj' param must be one of: %s" % ", ".join(self.OBJ_CHOICES)
            )
        obj_objs = self.OBJ_CHOICES[request.data["obj"]]
        obj_class = obj_objs[0]
        try:
            obj = obj_class.objects.get(id=request.data["id"])
        except obj_class.DoesNotExist, KeyError:
            raise ValidationError("'id' must be a valid object")
        
        obj.upvotes.remove(request.user)
        obj.downvotes.remove(request.user)
        
        vote_type = request.data.get("type")
        if vote_type == "upvote":
            obj.upvotes.add(request.user)
        elif vote_type == "downvote":
            obj.downvotes.add(request.user)
        return Response(obj_objs[1](obj).data)
        
        
class CourseViewSet(viewsets.ReadOnlyModelViewSet):    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
        
        
class InstructorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    
    
class DegreeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    
    
class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
        
        
class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return self.request.user.reviews.all()
    
    def perform_create(self, serializer):
        if serializer.validated_data['course'].id in \
           [r.course.id for r in self.request.user.reviews.all()]:
            raise ValidationError("Cannot submit multiple reviews for same course.")
            
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
        
        
class PlanViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = PlanSerializer
    
    def get_queryset(self):
        return self.request.user.plans.all()
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def perform_update(self, serializer):
        serializer.save(student=self.request.user)
        
        
class PlanYearViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = PlanYearSerializer
    
    def get_queryset(self):
        return PlanYear.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def perform_update(self, serializer):
        serializer.save(student=self.request.user)