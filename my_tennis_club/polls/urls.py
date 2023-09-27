from django.urls import path

from polls.views import StudentCall,LocationListAPI

urlpatterns = [
    # path("", views.index, name="index"),
    path("student/", StudentCall.as_view(), name="StudentCall"),
    path("location/", LocationListAPI.as_view(), name="LocationListAPI"),
]