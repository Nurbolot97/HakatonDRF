from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contacty/', ContactView.as_view(), name='contact'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-product-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_product_from_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQuantityView.as_view(), name='change_quantity'),

    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
]