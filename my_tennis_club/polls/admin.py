from django.contrib import admin

from .models import Product,Location,Time,Price,OTP

class ShowProduct(admin.ModelAdmin):
    list_display = ['product_name']
    
class ShowDistrict(admin.ModelAdmin):
    list_display = ['district','thana']

class ShowUser(admin.ModelAdmin):
    list_display = ['user_name']

class ShowPrice(admin.ModelAdmin):
    list_display = ['product_id_foreign','user_price','location_id_foreign','time_id_foreign']


admin.site.register(Product,ShowProduct)
admin.site.register(Location,ShowDistrict)
admin.site.register(Time)
admin.site.register(Price,ShowPrice)
admin.site.register(OTP)
# admin.site.register(User,ShowUser)