from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager

from api.models import Cart



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
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to = "photos/Y%/%m/%d/", null=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_user')

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
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )


    customer = models.ForeignKey(User, verbose_name='Покупатель', related_name='related_order', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    address = models.CharField(max_length=255, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    status = models.CharField(max_length=255, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=255, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    ordered_at = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)


