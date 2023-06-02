from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
import uuid
import os
from django.utils.text import slugify

def product_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('upload','products',filename)


class UserManeger(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email,password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManeger()

    USERNAME_FIELD = 'email'


class Merchant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = 'Merchants'

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Shop(models.Model):
    name = models.CharField(max_length=100, unique= True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    merchant = models.ForeignKey(Merchant , on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    description = models.TextField()
    active = models.BooleanField(default=False)
    connected_shops = models.ManyToManyField("self", through='ShopConnection', blank=True)
    # requested_shops = models.ManyToManyField('self', through='ShopConnection', blank = True)
    class Meta:
        verbose_name_plural = 'Shops'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
class ShopConnection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    ]

    sender_shop = models.ForeignKey(Shop, related_name='sent_connections', on_delete=models.CASCADE)
    receiver_shop = models.ForeignKey(Shop, related_name='received_connections', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shop Connections'

    def __str__(self):
        return f"Connection between {self.sender_shop} and {self.receiver_shop}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.sender_shop}{self.receiver_shop}')
        super().save(*args, **kwargs)

class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # image = models.ImageField(null=True, upload_to=product_image_file_path)
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)