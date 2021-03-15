from django.shortcuts import render
from .models import *
from user_accounts.models import User
from .mixins import CategoryMixin, CartMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView, ListView, DetailView, View
from django.http import HttpResponseRedirect
from django.contrib import messages


class MainPageView(CartMixin, TemplateView):

    def get(self, request, *args, **kwargs):
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
            'engine': engine,
            'cart': self.cart
            }
        return render(request, 'index.html', context)


class CategoryDetailView(CartMixin, CategoryMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'shop.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AboutUsView(CartMixin, CategoryMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_top()
        return render(request, 'about-us.html', locals())


class BlogView(CartMixin, CategoryMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_top()
        return render(request, 'blog.html', locals())


class ContactView(CartMixin, CategoryMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_top()
        return render(request, 'contact.html', locals())


class ProductDetailView(CartMixin, CategoryMixin, DetailView):

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        print(request)
        try:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            content_type = ContentType.objects.get(model=ct_model)
            product = content_type.model_class().objects.get(slug=product_slug)
            cart_product, created = CartProduct.objects.get_or_create(
                user = self.cart.owner,
                cart = self.cart,
                content_type = content_type,
                object_id = product.id
            )
            if created:
                self.cart.products.add(cart_product)
            self.cart.save()
            messages.add_message(request, messages.INFO, 'Товар успешно добавлен!')
            return HttpResponseRedirect('/cart/')
        except:
            return HttpResponseRedirect('/accounts/signup/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            content_type = ContentType.objects.get(model=ct_model)
            product = content_type.model_class().objects.get(slug=product_slug)
            cart_product= CartProduct.objects.get(
                user = self.cart.owner,
                cart = self.cart,
                content_type = content_type,
                object_id = product.id
            )
            self.cart.products.remove(cart_product)
            cart_product.delete()
            self.cart.save()
            messages.add_message(request, messages.INFO, 'Товар успешно удален!')
            return HttpResponseRedirect('/cart/')
        except:
            return HttpResponseRedirect('/accounts/signup/')


class ChangeQuantityView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            content_type = ContentType.objects.get(model=ct_model)
            product = content_type.model_class().objects.get(slug=product_slug)
            cart_product= CartProduct.objects.get(
                user = self.cart.owner,
                cart = self.cart,
                content_type = content_type,
                object_id = product.id
            )
            quantity = int(request.POST.get('quantity'))
            print(quantity)
            cart_product.quantity = quantity
            cart_product.save()
            self.cart.save()
            messages.add_message(request, messages.INFO, 'Количество успешно изменено!')
            return HttpResponseRedirect('/cart/')
        except:
            return HttpResponseRedirect('/accounts/signup/')


class CartView(CartMixin, CategoryMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_top()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'checkout.html', context)






