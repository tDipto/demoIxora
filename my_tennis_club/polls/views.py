from django.http import HttpResponse
from .serializers import StudentSerializer,LocationSerializer
from rest_framework.generics import ListAPIView
from .models import Student,Location



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class StudentCall(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class LocationListAPI(ListAPIView):
    model = Location
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
