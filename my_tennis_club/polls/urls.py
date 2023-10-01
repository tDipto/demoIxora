from django.urls import path

from . import views

urlpatterns = [

    path("location/", views.LocationAPI.as_view(), name="LocationAPI"),
    path("location/<int:id>/", views.LocationDetailAPI.as_view(), name="LocationDetailAPI"),

    path("product/", views.ProductAPI.as_view(), name="ProductAPI"),
    path("product/<int:id>/", views.ProductDetailAPI.as_view(), name="ProductDetailAPI"),

    path("user/", views.UserAPI.as_view(), name="UserAPI"),
    path("user/<int:id>/", views.UserDetailAPI.as_view(), name="UserDetailAPI"),

    path("price/", views.PriceAPI.as_view(), name="PriceAPI"),
    path("price/<int:id>/", views.PriceDetailAPI.as_view(), name="PriceDetailAPI"),

    path("getprice/<int:product_id>/<int:location_id>/", views.GetSingleAPI.as_view(), name="GetSingleAPI"),
    path("getallprice/<int:location_id>/", views.GetAllAPI.as_view(), name="GetAllAPI"),


    path("getGraph/<int:product_id>/<int:location_id>/", views.GetGraphAPI.as_view(), name="GetGraphAPI"),
]