from django.contrib import admin

from .models import Product,Location,Time,Price,User


admin.site.register(Product)
admin.site.register(Location)
admin.site.register(Time)
admin.site.register(Price)
admin.site.register(User)