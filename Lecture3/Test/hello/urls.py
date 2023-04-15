from django.urls import path
# import views from the same directory
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet")
]