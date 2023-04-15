from django.urls import path
# import views from the same directory
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
]