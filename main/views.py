from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import transaction

from .models import *
from .mixins import CategoryMixin, CartMixin
from django.contrib.contenttypes.models import ContentType
from .forms import OrderForm
from .utils import recalc_cart
from django.views.generic import (TemplateView, ListView, 
                                    DetailView, View)



class MainPageView(CartMixin, CategoryMixin, TemplateView):

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


class AddToCartView(CartMixin, CategoryMixin, View):

    def get(self, request, *args, **kwargs):
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
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Товар успешно добавлен!')
            return HttpResponseRedirect('/main/cart/')
        except:
            return HttpResponseRedirect('/main/cart/')


class DeleteFromCartView(CartMixin, CategoryMixin, View):

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
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Товар успешно удален!')
            return HttpResponseRedirect('/main/cart/')
        except:
            return HttpResponseRedirect('/main/cart/')


class ChangeQuantityView(CartMixin, CategoryMixin, View):

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
            cart_product.quantity = quantity
            cart_product.save()
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Количество успешно изменено!')
            return HttpResponseRedirect('/main/cart/')
        except:
            return HttpResponseRedirect('/main/cart/')


class CartView(CartMixin, CategoryMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_top()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'checkout.html', context)


class OrderView(CartMixin, CategoryMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_top()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'order.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        email = User.objects.get(email=request.user.email)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = email
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.ordered_at = form.cleaned_data['ordered_at']
            new_order.comment = form.cleaned_data['comment']
            new_order.cart = self.cart
            self.cart.in_order = True
            new_order.save()
            # self.cart.in_order = True
            # self.cart.save()
            # new_order.cart = self.cart
            # new_order.save()
            email.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Ваш заказ успешно оформлен!')
            return HttpResponseRedirect('/main/')
        return HttpResponseRedirect('/main/')












