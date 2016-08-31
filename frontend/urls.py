from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    url(r'^(?!api).*$', RedirectView.as_view(url='/'))
]
