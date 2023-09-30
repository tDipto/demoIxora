import datetime
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import ProductSerializer,LocationSerializer,UserSerializer,PriceSerializer,PriceSerializer2
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Product,Location,User,Price,Time
from django.db.models import Avg



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class LocationAPI(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'id'


class ProductAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class UserAPI(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
# 
# class PriceAPI(ListCreateAPIView):
#     queryset = Price.objects.all()
#     serializer_class = PriceSerializer

#     def perform_create(self, serializer):
#         time_instance = Time.objects.create()
#         serializer.save(time_id_foreign=time_instance)

class PriceAPI(ListCreateAPIView):
    queryset = Price.objects.all()
    # serializer_class = PriceSerializer


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


class PriceDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    lookup_field = 'id'

    
class GetSingleAPI(ListCreateAPIView):
    serializer_class = PriceSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Price.objects.filter(product_id_foreign=product_id)

    def get(self, request, product_id, location_id, year=None, month=None, day=None):
        location = Location.objects.get(id=location_id)
        product = Product.objects.get(id=product_id)


        year = request.query_params.get('year')
        month = request.query_params.get('month')
        day = request.query_params.get('day')

        # If no date criteria provided, use the current date
        if not (year or month or day):
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month
            day = current_date.day

        # Calculate the average user_price for the specified product_id, location_id, and date criteria
        queryset = Price.objects.filter(
            product_id_foreign=product_id,
            location_id_foreign=location_id
        )
        
        if year and month and day:
            # Filter by date criteria using Time objects
            queryset = queryset.filter(time_id_foreign__year=year, time_id_foreign__month=month, time_id_foreign__day=day)
        
        average_price = queryset.aggregate(avg_price=Avg('user_price'))
        
        response_data = {
            'place_name': location.district,  # Change this to the actual field name for place_name
            'product_name': product.product_name,
            'average_price': average_price['avg_price'],
            # 'year': int(year),
            # 'month': int(month),
            # 'day': int(day),
        }
        
        return Response(response_data)

