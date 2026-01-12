from django.urls import path
from .views import home, examples

from . import views


urlpatterns = [
    path("", home, name="home"),
    path("examples/", examples, name="examples-home"),
    path("examples/<slug:slug>/", examples, name="examples"),
    path("", views.home, name="home"),
    path("examples/", views.examples, name="examples-home"),
    path("examples/<slug:slug>/", views.examples, name="examples"),
]
