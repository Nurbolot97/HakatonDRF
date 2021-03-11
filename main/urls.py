from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('category/', CategoryListView.as_view(), name='category'),

]