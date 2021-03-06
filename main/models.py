from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from rest_framework_simplejwt.tokens import RefreshToken



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

    name_category = models.CharField(max_length=255, verbose_name='?????? ??????????????????')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return f"{self.name_category}"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='??????????????????')
    title = models.CharField(max_length=255, verbose_name='????????????????????????')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='??????????????????????')
    description = models.TextField(verbose_name='????????????????', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='????????')
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='??????????????????????', null=True)

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class CartProduct(models.Model):

    user = models.ForeignKey('User', verbose_name='????????????????????', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='??????????????', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='?????????? ????????')

    def __str__(self):
        return f"??????????????: {self.content_object.title} (?????? ??????????????)"

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.content_object.price
        super().save(*args, **kwargs)



class Cart(models.Model):

    owner = models.ForeignKey('User', null=True, on_delete=models.CASCADE, verbose_name='????????????????')
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='?????????? ????????')
    in_order = models.BooleanField(default=False)
    for_anonim_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"


class Wheel(Product):

    size = models.CharField(max_length=255, verbose_name='???????????? ????????')
    made_location = models.CharField(max_length=255, verbose_name='?????????? ????????????????????????')
    material = models.CharField(max_length=255, verbose_name='???????????????? ????????????????????????')
    
    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Engine(Product):

    power = models.CharField(max_length=255, verbose_name='????????????????')
    made_location = models.CharField(max_length=255, verbose_name='?????????? ????????????????????????')
    material = models.CharField(max_length=255, verbose_name='???????????????? ????????????????????????')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Comment(models.Model):

    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):  
        return f"Comment by {self.author} on {self.engine}"


class Display(Product):

    diagonal = models.CharField(max_length=255, verbose_name='??????????????????')
    display = models.CharField(max_length=255, verbose_name='?????? ??????????????')
    resolution = models.CharField(max_length=255, verbose_name='???????????????????? ????????????')
    ram = models.CharField(max_length=255, verbose_name='?????????????????????? ????????????')
   
    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Invalid email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
        
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be is staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be a superuser')
        return self._create_user(email, password, **extra_fields)
        

class User(AbstractUser):

    username = None
    email = models.EmailField(_('email_address'), unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to = "photos/Y%/%m/%d/", null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='???????????? ????????????????????', related_name='related_user')
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='??????????????????????', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'password2']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.email}"


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, '?????????? ??????????'),
        (STATUS_IN_PROGRESS, '?????????? ?? ??????????????????'),
        (STATUS_READY, '?????????? ??????????'),
        (STATUS_COMPLETED, '?????????? ????????????????')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, '??????????????????'),
        (BUYING_TYPE_DELIVERY, '????????????????')
    )


    customer = models.ForeignKey(User, verbose_name='????????????????????', related_name='related_order', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='??????')
    last_name = models.CharField(max_length=255, verbose_name='??????????????')
    phone = models.CharField(max_length=255, verbose_name='??????????????')
    address = models.CharField(max_length=255, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='??????????????')
    status = models.CharField(max_length=255, verbose_name='???????????? ????????????', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=255, verbose_name='?????? ????????????', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='?????????????????????? ?? ????????????', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='???????? ???????????????? ????????????')
    ordered_at = models.DateField(verbose_name='???????? ?????????????????? ????????????', default=timezone.now)

    def __str__(self):
        return str(self.id)



