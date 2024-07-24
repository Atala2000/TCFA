from django.shortcuts import render
from django.urls import include, path
from . import views

# Create your views here.
urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include("backend.api.urls")),
]
