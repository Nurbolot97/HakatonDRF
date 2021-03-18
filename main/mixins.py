from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.http import HttpResponseRedirect

from .models import Category, Wheel, Engine, Display, User, Cart


class CategoryMixin(SingleObjectMixin):

    CATEGORY_SLUG2PRODUCT_MODEL = {
        'wheels': Wheel,
        'engines': Engine,
        'displays': Display,
    }
    
    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_top()
            context['category_products'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_top()
        return context
        

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = User.objects.filter(email=request.user.email).first()
            if not customer:
                customer = Customer.objects.create(
                    email=request.user.email
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)     
        else:
            cart = Cart.objects.filter(for_anonim_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonim_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
     


                 
        
       
        
     





