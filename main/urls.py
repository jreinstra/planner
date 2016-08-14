from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reviews', views.ReviewViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    # API routes
    url(r'^search/$', views.Search.as_view(), name="api_search"),
    url(r'^courses/(?P<pk>[0-9]+)/$', views.CourseDetail.as_view(), name="api_course_detail"),
    url(r'^instructors/(?P<sunet>[\w-]+)/$', views.InstructorDetail.as_view(), name="api_instructor_detail"),
    
    # API router
    url(r'^', include(router.urls))
]