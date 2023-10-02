from django.urls import path

from . import views

urlpatterns = [

    path('signup/',views.UserSignupAPI.as_view(),name="UserSignupAPI"),
    path('signin/',views.SignInAPI.as_view(),name="SignInAPI"),
    path('signin/<str:username>',views.ShowSignInAPI.as_view(),name="ShowSignInAPI"),

    path('verify-otp/<str:username>/', views.OTPVerificationAPI.as_view(), name='otp-verification'),


    path("location/", views.LocationAPI.as_view(), name="LocationAPI"),
    path("location/<int:id>/", views.LocationDetailAPI.as_view(), name="LocationDetailAPI"),

    path("product/", views.ProductAPI.as_view(), name="ProductAPI"),
    path("product/<int:id>/", views.ProductDetailAPI.as_view(), name="ProductDetailAPI"),

    path("priceupdate/", views.PriceUpdateAPI.as_view(), name="PriceUpdateAPI"),

    path("getsingleproductprice/<int:product_id>/<int:location_id>/", views.GetSingleProductPriceAPI.as_view(), name="GetSingleProductPriceAPI"),
    path("getallproductprice/<int:location_id>/", views.GetAllProductPriceAPI.as_view(), name="GetAllProductPriceAPI"),


    path("getGraph/<int:product_id>/<int:location_id>/", views.GetGraphAPI.as_view(), name="GetGraphAPI"),
]