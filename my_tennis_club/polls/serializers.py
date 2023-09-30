from rest_framework import serializers
from .models import Location,Product,User,Price,Time

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class PriceSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['user_price', 'user_id_foreign', 'product_id_foreign', 'location_id_foreign']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['user_price', 'user_id_foreign', 'product_id_foreign', 'location_id_foreign', 'time_id_foreign']
        # depth = 1  # Include related fields up to a depth of 1
        