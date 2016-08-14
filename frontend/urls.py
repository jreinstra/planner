from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^', TemplateView.as_view(template_name="frontend/index.html"), name="index")
]