from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    phone = models.IntegerField(default=0)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # Add other fields as needed

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username






class User(models.Model):
    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField(default=0)
    # user_image = models.ImageField(upload_to='user_images/')
   

class Product(models.Model):
    product_id = models.IntegerField(default=0)
    product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    # product_image = models.ImageField(upload_to='user_images/')

class Location(models.Model):
    location_id = models.IntegerField(default=0)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=200)

class Time(models.Model):
    #  time_id = models.IntegerField(auto_now_add=True)
     year = models.PositiveIntegerField()
     month = models.PositiveIntegerField(default=0)
     day = models.CharField(max_length=200)

class Price(models.Model):
    price_id = models.IntegerField(default=0)
    user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_id_foreign = models.ForeignKey(User, on_delete=models.CASCADE)
    time_id_foreign = models.ForeignKey(Time, on_delete=models.CASCADE)
    product_id_foreign = models.ForeignKey(Product, on_delete=models.CASCADE)
    location_id_foreign = models.ForeignKey(Location, on_delete=models.CASCADE) 
 
        