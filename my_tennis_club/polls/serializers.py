from rest_framework import serializers
from .models import Location
#from .models import User
from .models import Product
from .models import Price
from .models import Time


from django.contrib.auth.models import User
from django.contrib.auth import password_validation


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




class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    year = serializers.IntegerField()



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'district','thana']

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['user_id', 'user_name','password','email','phone']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name','product_type','description','quantity']

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ['year', 'month','day']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['price_id', 'user_price','user_id_foreign','time_id_foreign','product_id_foreign','location_id_foreign']

