# from django.urls import path

# from polls.views import LocationListAPI

# urlpatterns = [
    # path("", views.index, name="index"),
    # path("student/", StudentCall.as_view(), name="StudentCall"),
     #path("location/", LocationListAPI.as_view(), name="LocationListAPI"),
    # path("user/", UserListAPI.as_view(), name="UserListAPI"),
    # path("time/",TimeListAPI.as_view(), name="TimeListAPI"),
    # #path("product/", ProductListAPI.as_view(), name="ProductListAPI"),
    # path("prices/", UserPricesAPI.as_view(), name="UserPricesAPI"),
    #path('signup/', views.signup, name='signup'),
    #]

# urlpatterns = [
 
#     path('admin/', admin.site.urls),
 
#     ##### user related path##########################
#     path('', include('user.urls')),
#     path('login/', user_view.Login, name ='login'),
#     path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
#     path('register/', user_view.register, name ='register'),
 
# ]
from django.urls import path
from polls.views import UserSignupAPI,SignInAPI,LocationListAPI,ProductAPI,ShowSignInAPI
from . import views
urlpatterns = [
    # ... other URL patterns for your app ...
    path('signup/', UserSignupAPI.as_view(), name='signup'),

    path('signin/',views.SignInAPI.as_view(),name="SignInAPI"),
    path('signin/<str:username>',views.ShowSignInAPI.as_view(),name="ShowSignInAPI"),

    path("location/<int:id>/", LocationListAPI.as_view(), name="LocationListAPI"),

    path("product/", views.ProductAPI.as_view(), name="ProductAPI"),
    path("product/<int:id>/", views.ProductDetailAPI.as_view(), name="ProductDetailAPI"),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
