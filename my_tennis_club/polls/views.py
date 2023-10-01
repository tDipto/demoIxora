from django.http import HttpResponse
from .serializers import LocationSerializer,UserSerializer,ProductSerializer,PriceSerializer,TimeSerializer,LoginSerializer,UserRegistrationSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Location,User,Product,Price,Time
from django.db.models import Max, Avg, Min
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.db import IntegrityError
from .models import User, OTP
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class LocationListAPI(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field='id'


class UserListAPI(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field='id'


class ProductListAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field='id'


class PriceListAPI(ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

class PriceDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    lookup_field='id'


class TimeListAPI(ListCreateAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer

class TimeDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    lookup_field='id'


class ProductPriceSummaryView(View):
    def get(self, request, product_id, location_id, time_id):
        try:
            product = Product.objects.get(id=product_id)
            location = Location.objects.get(id=location_id)
            time = Time.objects.get(id=time_id)


            prices = Price.objects.filter(
                product_id_foreign=product,
                location_id_foreign=location,
                time_id_foreign=time
            )

            max_price = prices.aggregate(Max('user_price'))['user_price__max']
            avg_price = prices.aggregate(Avg('user_price'))['user_price__avg']
            min_price = prices.aggregate(Min('user_price'))['user_price__min']

        
            response_data = {
                'max_price': max_price,
                'avg_price': avg_price,
                'min_price': min_price,
            }

            return JsonResponse(response_data)
        except (Product.DoesNotExist, Location.DoesNotExist, Time.DoesNotExist):
            
            return JsonResponse({'error': 'One or more objects not found'}, status=404)



class UserSignupAPI(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                # Generate OTP (example: 6-digit OTP)
                otp_code = generate_random_otp()

                # Store OTP in the database
                OTP.objects.create(user=user, otp_code=otp_code)

                # Send OTP to the user via email or SMS (implement this)
                send_otp_to_user(user.email, otp_code)  # Replace with your email/SMS sending logic

                return Response({"message": "User registered successfully. Check your email/SMS for OTP."},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"message": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPEmail(APIView):
    def post(self, request):
        try:
            otp_code = request.data.get("otp_code")
            user = request.user  # Assuming the user is authenticated

            # Check if the provided OTP matches the stored OTP for the user
            otp_obj = get_object_or_404(OTP, user=user, otp_code=otp_code)

            # Mark the user as verified (you can set a flag in the User model)
            user.is_verified = True
            user.save()

            # Optionally, delete the OTP record or mark it as used
            otp_obj.delete()

            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        except OTP.DoesNotExist:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user =  authenticate(email = email,password = password)
            
                if user is None:
                    return Response(
                    {
                    'status' : 400,
                    'message' : 'Invalid password',
                    'data' : {}
                })

                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
                
            return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data' : serializer.errors
            })
        
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': {}
            })

