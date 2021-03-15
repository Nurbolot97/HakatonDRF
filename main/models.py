from django.db import models
from user_accounts.models import User
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Wheels': 'wheel__count',
        'Engines': 'engine__count',
        'Displays': 'display__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_top(self):
        models = get_models_for_count('wheel', 'engine', 'display')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name_category, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name_category]))
            for c in qs
        ]
        return data



class Category(models.Model):

    name_category = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return f"{self.name_category}"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})



class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class CartProduct(models.Model):

    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f"Продукт: {self.content_object.title} (для корзины)"

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.content_object.price
        super().save(*args, **kwargs)



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
        cart_data = self.products.aggregate(models.Sum('final_price'), models.Count('id'))
        if cart_data.get('final_price__sum'):
            self.final_price = cart_data['final_price__sum']
        else:
            self.final_price = 0
        self.total_products = cart_data['id__count']
        super().save(*args, **kwargs)


class Wheel(Product):

    size = models.CharField(max_length=255, verbose_name='Размер шины')
    made_location = models.CharField(max_length=255, verbose_name='Место производства')
    material = models.CharField(max_length=255, verbose_name='Материал производства')
    
    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Engine(Product):

    power = models.CharField(max_length=255, verbose_name='Мощность')
    made_location = models.CharField(max_length=255, verbose_name='Место производства')
    material = models.CharField(max_length=255, verbose_name='Материал производства')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Display(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
   
    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')



