from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("examples/", views.examples, name="examples-home"),
    path("examples/<slug:slug>/", views.examples, name="examples"),
]
