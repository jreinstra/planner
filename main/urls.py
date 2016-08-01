from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="main/index.html"), name="index"),
    url(r'^search/$', views.search, name="search"),
]