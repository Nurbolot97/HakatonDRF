from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


from .api_views import ( CategoryApiView, EnginesListApiView, DisplayListApiView,
                        WheelListApiView, EngineDetailApiView, DisplayDetailApiView, 
                        WheelDetailApiView, UsersListApiView, CategoryListApiView,
                        CategoryCreateApiView, activate, register, RequestPasswordResetEmail,
                        PasswordTokenCheckAPI, SetNewPasswordAPIView, EngineCreateApiView,
                        EngineUpdateApiView, EngineDestroyApiView, CommentListApiView,
                        CommentCreateApiView, CommentDestroyApiView
                        )


urlpatterns = [
    path('account/register/', register, name='register'),
    path('account/activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('account/user-list/', UsersListApiView.as_view(), name='user_list'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/password-reset/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('account/password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('account/password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),


    path('home/category/', CategoryListApiView.as_view(), name='category_list'),
    path('home/category-create/', CategoryCreateApiView.as_view(), name='category_create'),
    path('home/category/<str:id>/', CategoryApiView.as_view(), name='category'),

    path('product/engine-create/', EngineCreateApiView.as_view(), name='engine-create'),
    path('product-engine-list/', EnginesListApiView.as_view(), name='engine_list'),
    path('product-engine-detail/<str:id>/', EngineDetailApiView.as_view(), name='engine_detail'),
    path('product-engine-update/<str:id>/', EngineUpdateApiView.as_view(), name='engine-update'),
    path('product-engine-destroy/<str:id>/', EngineDestroyApiView.as_view(), name='engine-destroy'),
    
    path('comments/', CommentListApiView.as_view(), name='comments'),
    path('comments-create/', CommentCreateApiView.as_view(), name='comments_create'),
    path('comments-destroy/<str:id>/', CommentDestroyApiView.as_view(), name='comment-destroy'),

    path('product-display-list/', DisplayListApiView.as_view(), name='display_list'),
    path('product-wheel-list/', WheelListApiView.as_view(), name='wheel_list'),
    
    path('product-display-list/<str:id>/', DisplayDetailApiView.as_view(), name='display_detail'),
    path('product-wheel-list/<str:id>/', WheelDetailApiView.as_view(), name='wheel_detail'),
]