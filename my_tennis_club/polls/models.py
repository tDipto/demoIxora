from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



######################################################################## 
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='img/',max_length=250,null=True,default=None)

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
    


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.otp} (Verified: {self.is_verified})"