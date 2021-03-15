from django.urls import path
from .api_views import (register, activate, CategoryListApiView, 
                        EnginesListApiView, DisplayListApiView,
                        WheelListApiView, EngineDetailApiView,
                        DisplayDetailApiView, WheelDetailApiView,
                        UsersListApiView
                        )



urlpatterns = [
    path('account/register/', register, name='register'),
    path('account/activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('account/user-list/', UsersListApiView.as_view(), name='user_list'),
    path('home/category-list/', CategoryListApiView.as_view(), name='category_list'),
    path('home/product-engine-list/', EnginesListApiView.as_view(), name='engine_list'),
    path('home/product-display-list/', DisplayListApiView.as_view(), name='display_list'),
    path('home/product-wheel-list/', WheelListApiView.as_view(), name='wheel_list'),
    path('home/product-engine-list/<str:id>/', EngineDetailApiView.as_view(), name='engine_detail'),
    path('home/product-display-list/<str:id>/', DisplayDetailApiView.as_view(), name='display_detail'),
    path('home/product-wheel-list/<str:id>/', WheelDetailApiView.as_view(), name='wheel_detail'),
]