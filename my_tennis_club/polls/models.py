from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

########################################################################


class Student(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()



########################################################################    #
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