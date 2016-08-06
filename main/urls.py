from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Main pages
    url(r'^$', TemplateView.as_view(template_name="main/index.html"), name="index"),
    url(r'^courses/(?P<pk>[0-9]+)/$', views.CourseDetailView.as_view(), name='course_detail'),
    
    # API routes
    url(r'^api/search/$', views.Search.as_view(), name="api_search"),
    url(r'^api/courses/(?P<pk>[0-9]+)/$', views.CourseDetail.as_view(), name="api_course_detail"),
]