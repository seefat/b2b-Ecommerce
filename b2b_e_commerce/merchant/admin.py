from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Merchant)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ShopConnection)