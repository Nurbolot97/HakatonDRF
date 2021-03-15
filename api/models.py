from django.db import models


from user_accounts.models import User
from main.models import CartProduct




class Cart(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonim_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        if not self.id:
            super(Cart, self).save(*args, **kwargs)
        super(Cart, self).save(*args, **kwargs)
        cart_data = self.products.aggregate(models.Sum('final_price'), models.Count('id'))
        if cart_data.get('final_price__sum'):
            self.final_price = cart_data['final_price__sum']
        else:
            self.final_price = 0
        self.total_products = cart_data['id__count']
        super().save(*args, **kwargs)



