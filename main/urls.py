from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, base_name="reviews")
router.register(r'comments', views.CommentViewSet, base_name="comments")
router.register(r'instructors', views.InstructorViewSet, base_name="instructors")
router.register(r'courses', views.CourseViewSet, base_name="courses")

urlpatterns = [
    # API routes
    url(r'^search/$', views.Search.as_view(), name="api_search"),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^vote/$', views.Vote.as_view(), name="vote"),
    
    # API router
    url(r'^', include(router.urls))
]