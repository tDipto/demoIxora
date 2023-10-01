from rest_framework import serializers
from .models import Location,Product,User,Price
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core import exceptions

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
        
class PriceSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['user_price', 'user_id_foreign', 'product_id_foreign', 'location_id_foreign']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['user_price', 'user_id_foreign', 'product_id_foreign', 'location_id_foreign', 'time_id_foreign']
        # depth = 1  # Include related fields up to a depth of 1



class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")

        
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("Email address is already in use.")
 
     
        try:
            password_validation.validate_password(data.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(str(e))

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
