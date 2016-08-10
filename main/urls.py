from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # API routes
    url(r'^api/search/$', views.Search.as_view(), name="api_search"),
    url(r'^api/courses/(?P<pk>[0-9]+)/$', views.CourseDetail.as_view(), name="api_course_detail"),
    url(r'^api/instructors/(?P<sunet>[\w-]+)/$', views.InstructorDetail.as_view(), name="api_instructor_detail"),
]