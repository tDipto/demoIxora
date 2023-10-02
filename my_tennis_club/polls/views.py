import datetime
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import ProductSerializer,LocationSerializer,PriceSerializer,PriceSerializer2,UserSerializer,CustomTokenObtainPairSerializer,ShowUserSerializer,OTPVerificationSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from .models import Product,Location,Price,Time,OTP
from django.db.models import Avg, Max, Min
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework_jwt.authentication import JSONWebTokenAuthenticationV2 as JSONWebTokenAuthentication


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserSignupAPI(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "User registered successfully."})
    #     return Response(serializer.errors)


class SignInAPI(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ShowSignInAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ShowUserSerializer
    lookup_field = 'username'

class LocationAPI(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

class LocationDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'id'


class ProductAPI(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPI(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    


class PriceUpdateAPI(ListCreateAPIView):
    queryset = Price.objects.all()


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PriceSerializer2
        return PriceSerializer 


    def perform_create(self, serializer):
        current_datetime = datetime.datetime.now()

        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        hour = current_datetime.hour

        try:
            current_time = Time.objects.get(year=year, month=month, day=day, hour=hour)
        except Time.DoesNotExist:
            current_time = Time.objects.create(
                year=year,
                month=month,
                day=day,
                hour=hour
            )
    
        serializer.save(
            time_id_foreign=current_time
        )

    
class GetSingleProductPriceAPI(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PriceSerializer


    def get(self, request, product_id, location_id, year=None, month=None, day=None):
        location = Location.objects.get(id=location_id)
        product = Product.objects.get(id=product_id)


        year = request.query_params.get('year')
        month = request.query_params.get('month')
        day = request.query_params.get('day')

        if not (year or month or day):
            current_date = datetime.datetime.now()
            year = current_date.year
            month = current_date.month
            day = current_date.day

        queryset = Price.objects.filter(
            product_id_foreign=product_id,
            location_id_foreign=location_id
        )
        
        if year:
            queryset = queryset.filter(time_id_foreign__year=year)
        if year and month:
            queryset = queryset.filter(time_id_foreign__month=month)
        if year and month and day:
            queryset = queryset.filter(time_id_foreign__day=day)
        
        price_stats = queryset.aggregate(
                avg_price=Avg('user_price'),
                max_price=Max('user_price'),
                min_price=Min('user_price')
            )
 
        response_data = {
            'place_name': location.district, 
            'product_name': product.product_name,
            'average_price': price_stats['avg_price'],
            'max_price': price_stats['max_price'],
            'min_price': price_stats['min_price'],
            'year': int(year) if year else None,
            'month': int(month) if month else None,
            'day': int(day) if day else None,
        }
    
        return Response(response_data)
    


class GetAllProductPriceAPI(ListCreateAPIView):
    serializer_class = PriceSerializer

    def get_queryset(self):
        pass

    def get(self, request, location_id, year=None, month=None, day=None):
        location = Location.objects.get(id=location_id)
        products = Product.objects.all()
        result = []

        year = request.query_params.get('year')
        month = request.query_params.get('month')
        day = request.query_params.get('day')

        if not (year or month or day):
            current_date = datetime.datetime.now()
            year = current_date.year
            month = current_date.month
            day = current_date.day

        response_data = {
            'location': location.district,
            'year': int(year) if year else None,
            'month': int(month) if month else None,
            'day': int(day) if day else None,
            'products': []
        }

        queryset = Price.objects.filter(location_id_foreign=location_id)
        if year:
            queryset = queryset.filter(time_id_foreign__year=year)
        if month:
            queryset = queryset.filter(time_id_foreign__month=month)
        if day:
            queryset = queryset.filter(time_id_foreign__day=day)

        for product in products:
            queryset = queryset.filter(product_id_foreign=product.id)

            price_stats = queryset.aggregate(
                avg_price=Avg('user_price'),
                max_price=Max('user_price'),
                min_price=Min('user_price')
            )

            product_data = {
                'product_name': product.product_name,
                'average_price': price_stats['avg_price'],
                'max_price': price_stats['max_price'],
                'min_price': price_stats['min_price'],
            }


            response_data['products'].append(product_data)

        result.append(response_data)

        return Response(result)





class GetGraphAPI(ListCreateAPIView):
    serializer_class = PriceSerializer

    def get(self, request, product_id, location_id, Syear=None, Eyear=None, Smonth=None, Emonth=None, Sday=None, Eday=None):
        location = Location.objects.get(id=location_id)
        product = Product.objects.get(id=product_id)

        Syear = request.query_params.get('Syear')
        Eyear = request.query_params.get('Eyear')
        Smonth = request.query_params.get('Smonth')
        Emonth = request.query_params.get('Emonth')
        Sday = request.query_params.get('Sday')
        Eday = request.query_params.get('Eday')

        response_data = {
            'product': product.product_name,
            'location': location.district,
            'date_range_stats': {}
        }

        def generate_stats(queryset):
            price_stats = queryset.aggregate(
                avg_price=Avg('user_price'),
                max_price=Max('user_price'),
                min_price=Min('user_price')
            )

            return {
                'max_price': price_stats['max_price'],
                'min_price': price_stats['min_price'],
                'avg_price': price_stats['avg_price'],
            }

        def process_date_range(queryset, date_range_key):
            if date_range_key not in response_data['date_range_stats']:
                response_data['date_range_stats'][date_range_key] = generate_stats(queryset)

        if not Eyear:
            if not Syear:
                if not Emonth:
                    # Smonth/day - Smonth/day
                    for m in range(int(Smonth), int(Smonth) + 1):
                        for d in range(int(Sday), int(Eday) + 1):
                            queryset = Price.objects.filter(
                                product_id_foreign=product_id,
                                location_id_foreign=location_id,
                                time_id_foreign__month=m,
                                time_id_foreign__day=d
                            )

                            process_date_range(queryset, f'{m}-{d}')
                else:
                    # Smonth - Emonth
                    for m in range(int(Smonth), int(Emonth) + 1):
                        queryset = Price.objects.filter(
                            product_id_foreign=product_id,
                            location_id_foreign=location_id,
                            time_id_foreign__month=m,
                        )

                        process_date_range(queryset, f'{m}')
            else:
                # Syear/month - Syear/month
                for y in range(int(Syear), int(Syear) + 1):
                    for m in range(int(Smonth), int(Emonth) + 1):
                        queryset = Price.objects.filter(
                            product_id_foreign=product_id,
                            location_id_foreign=location_id,
                            time_id_foreign__year=y,
                            time_id_foreign__month=m
                        )

                        process_date_range(queryset, f'{y}-{m}')
        else:
            for y in range(int(Syear), int(Eyear) + 1):
                queryset = Price.objects.filter(
                    product_id_foreign=product_id,
                    location_id_foreign=location_id,
                    time_id_foreign__year=y
                )

                process_date_range(queryset, f'{y}')

        return Response(response_data)


        

from django.shortcuts import get_object_or_404


class OTPVerificationAPI(GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def put(self, request, username, *args, **kwargs):
        otp_entry = get_object_or_404(OTP, user__username=username)

        
        if 'otp' not in request.data:
            return Response({'detail': 'OTP is required in the request'})

        serializer = self.get_serializer(otp_entry, data=request.data, partial=True)

        if serializer.is_valid():
            if serializer.validated_data.get('otp') == otp_entry.otp:
                otp_entry.is_verified = True
                otp_entry.save()
                return Response({'detail': 'OTP verification successful'})
            else:
                return Response({'detail': 'Invalid OTP'})
        return Response(serializer.errors)