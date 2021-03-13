from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contacty/', ContactView.as_view(), name='contact'),
    path('cart/', CartView.as_view(), name='cart'),

    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
]