from django.http import HttpResponse
from .serializers import LocationSerializer,ProductSerializer,PriceSerializer,TimeSerializer
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Location,User,Product,Price,Time
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from django.db import IntegrityError

class UserSignupAPI(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"message": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate

class UserLoginAPI(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class StudentCall(ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

# class LocationListAPI(ListAPIView):
#     model = Location
#     serializer_class = LocationSerializer
#     queryset = Location.objects.all()

# class UserListAPI(ListAPIView):
#     model = User
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

# class TimeListAPI(ListAPIView):
#     model = Time
#     serializer_class = TimeSerializer
#     queryset = Time.objects.all()


# class UserPricesAPI(ListAPIView):
#     serializer_class = PriceSerializer
#     def get_queryset(self):
#         user_id = self.request.query_params.get('user_id_foreign')
#         if user_id is not None:
#             return Price.objects.filter(user_id=user_id)
#         return Price.objects.all()  # Return an empty queryset if user_id is not provided


# class LocationListAPI(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
#     serializer_class = LocationSerializer
#     lookup_field = 'location_id'

#     def get_queryset(self):
#         location_id = self.request.query_params.get('location_id')
#         if location_id is not None:
#             return Location.objects.filter(location_id=location_id)
#         return Location.objects.all()
    

#     def delete(self, request, *args, **kwargs):
#         location_id = self.request.query_params.get('location_id')
#         if location_id is None:
#             return Response({'detail': 'location_id query parameter is required.'})

#         try:
#             location = Location.objects.get(location_id=location_id)
#             location.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Location.DoesNotExist:
#             return Response({'detail': 'Location not found.'})
        
#     def put(self, request, *args, **kwargs):
#         location_id = self.request.query_params.get('location_id')
#         if location_id is None:
#             return Response({'detail': 'location_id query parameter is required.'})

#         try:
#             location = Location.objects.get(location_id=location_id)
#             serializer = self.get_serializer(location, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors)
#         except Location.DoesNotExist:
#             return Response({'detail': 'Location not found.'})
