from django.urls import path
from .api_views import register, activate



urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]