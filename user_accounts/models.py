from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


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
    # photo = models.ImageField(upload_to = "photos/Y%/%m/%d/", null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'password2']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.email}"

