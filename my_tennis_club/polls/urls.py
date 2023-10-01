from django.urls import path

from polls.views import LocationListAPI,LocationDetailAPI,PriceListAPI,PriceDetailAPI,ProductListAPI,ProductDetailAPI,TimeListAPI,TimeDetailAPI,UserListAPI,UserDetailAPI,ProductPriceSummaryView,UserSignupAPI,VerifyOTPEmail

urlpatterns = [
    # path("", views.index, name="index"),
    path("user/", UserListAPI.as_view(), name="UserListAPI"),
    path('users/<int:id>/', UserDetailAPI.as_view(), name='user-detail'),

    path("location/", LocationListAPI.as_view(), name="LocationListAPI"),
    path('locations/<int:id>/', LocationDetailAPI.as_view(), name='location-detail'),

    path("price/", PriceListAPI.as_view(), name="PriceListAPI"),
    path('prices/<int:id>/', PriceDetailAPI.as_view(), name='price-detail'),

    path("product/", ProductListAPI.as_view(), name="ProductListAPI"),
    path('products/<int:id>/', ProductDetailAPI.as_view(), name='product-detail'),

    path("time/", TimeListAPI.as_view(), name="TimeListAPI"),
    path('times/<int:id>/', TimeDetailAPI.as_view(), name='time-detail'),

    path('product-price-summary/<int:product_id>/<int:location_id>/<int:time_id>/', ProductPriceSummaryView.as_view(), name='product_price_summary'),

    # path('login/', LoginAPI.as_view(),name = "LoginAPI"),
    # path("product-price-summary/", product_price_summary.as_view(), name="product_price_summary"),
    # path('product-price-summaries/<int:id>/', product_price_summary.as_view(), name='product_price_summary_detail'),

      path('signup/',UserSignupAPI.as_view(), name = 'signup'),
      path('verify-otp/', VerifyOTPEmail.as_view(), name='verify_otp'),
]