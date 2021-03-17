from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


from .api_views import ( CategoryApiView, EnginesListApiView, DisplayListApiView,
                        WheelListApiView, EngineDetailApiView, DisplayDetailApiView, 
                        WheelDetailApiView, UsersListApiView, CategoryListApiView,
                        CategoryCreateApiView, activate, register, RequestPasswordResetEmail,
                        PasswordTokenCheckAPI, SetNewPasswordAPIView
                        )


urlpatterns = [
    path('account/register/', register, name='register'),
    path('account/activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('account/user-list/', UsersListApiView.as_view(), name='user_list'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('account/password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('account/password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),

    path('home/category-list/', CategoryListApiView.as_view(), name='category_list_create'),
    path('home/category-create/', CategoryCreateApiView.as_view(), name='category_create'),
    path('home/category/<str:id>/', CategoryApiView.as_view(), name='category'),

    path('home/product-engine-list/', EnginesListApiView.as_view(), name='engine_list'),
    path('home/product-display-list/', DisplayListApiView.as_view(), name='display_list'),
    path('home/product-wheel-list/', WheelListApiView.as_view(), name='wheel_list'),
    path('home/product-engine-list/<str:id>/', EngineDetailApiView.as_view(), name='engine_detail'),
    path('home/product-display-list/<str:id>/', DisplayDetailApiView.as_view(), name='display_detail'),
    path('home/product-wheel-list/<str:id>/', WheelDetailApiView.as_view(), name='wheel_detail'),
]