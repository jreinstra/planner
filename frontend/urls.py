from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^(?!api).*$', TemplateView.as_view(template_name="frontend/index.html"), name="index")
]
