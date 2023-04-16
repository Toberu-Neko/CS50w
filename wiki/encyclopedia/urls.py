from django.urls import path

from . import views

# app_name="wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index),
    path("wiki/", views.index),
    path("wiki/<str:title>", views.gotoTitle, name="gotoTitle"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    
    path("search/", views.search, name="search"),
    
    path("create/", views.create, name="create"),
    
    path("random/", views.randomWiki, name="random"),
]
