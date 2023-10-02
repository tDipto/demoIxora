import random
from rest_framework import serializers
from .models import Location,Product,Price,OTP
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail

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


# class UserSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only=True, required=True)
#     email = serializers.EmailField(required=True)
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def validate(self, data):
#         if data.get('password') != data.get('confirm_password'):
#             raise serializers.ValidationError("Passwords do not match.")

#         if User.objects.filter(username=data['username']).exists():
#             raise serializers.ValidationError("This username is already in use.")

#         if User.objects.filter(email=data['email']).exists():
#             raise serializers.ValidationError("This email is already in use.")

#         return data

#     def create(self, validated_data):
#         validated_data.pop('confirm_password', None)
#         user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
#         user.email = validated_data['email']
#         user.first_name = validated_data['first_name']
#         user.last_name = validated_data['last_name']
#         user.save()

#         # Send email notification
#         subject = 'Registration Successful'
#         message = 'Thank you for registering!'
#         recipients = [user.email]
#         send_mail(subject, message, settings.EMAIL_HOST_USER, recipients)

#         return user



class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("This username is already in use.")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("This email is already in use.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        # Generate a random 4-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        # Create an OTP entry for the user
        otp_entry, created = OTP.objects.get_or_create(user=user)
        otp_entry.otp = otp
        otp_entry.save()

        # Send email notification with OTP
        subject = 'OTP for Registration'
        message = f'Your OTP for registration is: {otp}'
        recipients = [user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients)

        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if user is None:
                raise serializers.ValidationError(
                    "No user with the provided username and password was found."
                )
        else:
            raise serializers.ValidationError(
                "Both username and password are required fields."
            )

        data = super().validate(attrs)
        return data

class ShowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['otp', 'is_verified']