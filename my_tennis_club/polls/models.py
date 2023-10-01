from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password



########################################################################    #

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

    def _str_(self):
        return self.username


# class User(models.Model):
#     user_name = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     phone = models.IntegerField(default=0)
#     # user_image = models.ImageField(upload_to='user_images/')
   
#     def __str__(self):
#         return self.user_name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    # product_image = models.ImageField(upload_to='user_images/')
    def __str__(self):
        return self.product_name

class Location(models.Model):
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=200)

    def __str__(self):
        return f"district: {self.district}, thana: {self.thana}"    

class Time(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()
    hour = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"year: {self.year}, month: {self.month}, day: {self.day}, hour: {self.hour}"

class Price(models.Model):
    user_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_id_foreign = models.ForeignKey(User, on_delete=models.CASCADE)
    time_id_foreign = models.ForeignKey(Time, on_delete=models.CASCADE)
    product_id_foreign = models.ForeignKey(Product, on_delete=models.CASCADE)
    location_id_foreign = models.ForeignKey(Location, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Product: {self.product_id_foreign},Price: {self.user_price}, Location: {self.location_id_foreign}, Time: {self.time_id_foreign}"
