from django.http import HttpResponse
from .serializers import LocationSerializer,ProductSerializer,PriceSerializer,TimeSerializer,UserSerializer,CustomTokenObtainPairSerializer
from .serializers import ShowUserSerializer
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Location,User,Product,Price,Time
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework_jwt.authentication import JSONWebTokenAuthenticationV2 as JSONWebTokenAuthentication


class UserSignupAPI(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignInAPI(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ShowSignInAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ShowUserSerializer
    lookup_field = 'username'



class ProductAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class LocationListAPI(RetrieveUpdateDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            location = Location.objects.get(pk=id)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({"message": "Location not found"}, status=404)

# class StudentCall(ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

# class LocationListAPI(RetrieveUpdateDestroyAPIView):
#     model = Location
#     serializer_class = LocationSerializer
#     queryset = Location.objects.all()
#     lookup_field = 'id'


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
