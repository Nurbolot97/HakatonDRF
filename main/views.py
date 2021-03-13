from django.shortcuts import render
from .models import *
from user_accounts.models import User
from .mixins import CategoryMixin
from django.views.generic import TemplateView, ListView, DetailView, View


class MainPageView(TemplateView):

    def get(self, request):
        categories = Category.objects.get_categories_for_top()
        wheels = LatestProducts.objects.get_products_for_main_page('wheel')[:4]
        diplayes = LatestProducts.objects.get_products_for_main_page('display')[:4]
        engines = LatestProducts.objects.get_products_for_main_page('engine')[:4]
        wheel = LatestProducts.objects.get_products_for_main_page('wheel')[:1]
        diplay = LatestProducts.objects.get_products_for_main_page('display')[:1]
        engine = LatestProducts.objects.get_products_for_main_page('engine')[:1]
        context = {
            'categories': categories, 
            'wheels': wheels,
            'displayes': diplayes,
            'engines': engines,
            'wheel': wheel,
            'display': diplay,
            'engine': engine
    
            }
        return render(request, 'index.html', context)


class CategoryDetailView(CategoryMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'shop.html'
    slug_url_kwarg = 'slug'


class AboutUsView(CategoryMixin, View):

    def get(self, request):
        categories = Category.objects.get_categories_for_top()
        return render(request, 'about-us.html', locals())


class BlogView(CategoryMixin, TemplateView):

    def get(self, request):
        categories = Category.objects.get_categories_for_top()
        return render(request, 'blog.html', locals())


class ContactView(CategoryMixin, TemplateView):

    def get(self, request):
        categories = Category.objects.get_categories_for_top()
        return render(request, 'contact.html', locals())


class ProductDetailView(CategoryMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'wheel': Wheel,
        'engine': Engine,
        'display': Display
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    template_name = 'single-product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class CartView(CategoryMixin, View):

    def get(self, request, *args, **kwargs):
        customer = User.objects.get(email=request.user.email)
        cart = CartProduct.objects.filter(user=customer)
        categories = Category.objects.get_categories_for_top()
        context = {
            'cart': cart,
            'categories': categories
        }
        return render(request, 'checkout.html', context)






