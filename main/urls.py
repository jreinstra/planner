from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, base_name="reviews")
router.register(r'comments', views.CommentViewSet, base_name="comments")

router.register(r'instructors', views.InstructorViewSet, base_name="instructors")
router.register(r'courses', views.CourseViewSet, base_name="courses")
router.register(r'degrees', views.DegreeViewSet, base_name="degrees")
router.register(r'departments', views.DepartmentViewSet, base_name="departments")

router.register(r'public_plans', views.PublicPlanViewSet, base_name="public_plans")
router.register(r'public_plan_years', views.PublicPlanYearViewSet, base_name="public_plan_years")

router.register(r'plans', views.PlanViewSet, base_name="plans")
router.register(r'plan_years', views.PlanYearViewSet, base_name="plan_years")

router.register(r'user', views.UserViewSet, base_name="user")

urlpatterns = [
    # API routes
    url(r'^search/$', views.Search.as_view(), name="search"),
    url(r'search_degrees/$', views.SearchDegrees.as_view(), name="search_degrees"),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^vote/$', views.Vote.as_view(), name="vote"),
    url(r'^stats/$', views.PlannerStats.as_view(), name="stats"),
    
    url(r'^star/$', views.Star.as_view(), name="star"),
    url(r'^starred/$', views.Starred.as_view(), name="starred"),
    
    # API router
    url(r'^', include(router.urls))
]