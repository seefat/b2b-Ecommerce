from django.contrib.auth import (
    get_user_model,
    authenticate,
)
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext as _
from rest_framework import serializers
from merchant.models import *
def get_merchant_name(request):
    user = request.user
    if user.is_authenticated:
        try:
            merchant = user.merchant
            return merchant.name
        except Merchant.DoesNotExist:
            return None
    return None
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    extra_kwargs = {'password':{'write_only':True,'min_length':5}}

    def create(self, validated_data):
        if validated_data['password1'] != validated_data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    extra_kwargs = {'password':{'write_only':True,'min_length':5}}
class MerchantSerializer(serializers.Serializer):
    name = serializers.CharField()
    dob = serializers.DateField()

    def create(self, validated_data):
        merchant = Merchant.objects.create(
            user = self.context['request'].user,
            name=validated_data['name'],
            dob=validated_data['dob']
        )
        return merchant
        # return Merchant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.get('dob', instance.dob)
        def create(self, validated_data):
            merchant = Merchant.objects.create(
                name=validated_data['name'],
                dob=validated_data['dob'],
            )
            return merchant
        # return Merchant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.save()
        return instance

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    slug = serializers.SlugField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        def create(self, validated_data):
            merchant = Merchant.objects.create(
                name=validated_data['name'],
                dob=validated_data['dob']
            )
            return merchant
        # return Merchant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.save()
        return instance

class ShopSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    merchant = serializers.CharField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    address = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField(default=False)
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        user=validated_data.pop('user')
        mechant=Merchant.objects.get(user=user)

        category = Category.objects.get(id=category_id)
        shop = Shop.objects.create(category=category, merchant=mechant,**validated_data)
        return shop
        # return Merchant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

class MyShopSerializer(ShopSerializer):
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        user=validated_data.pop('user')
        mechant=Merchant.objects.get(user=user)
        category = Category.objects.get(id=category_id)
        shop = Shop.objects.create(category=category, merchant=mechant,**validated_data)
        return shop
        # return Merchant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
class MyShopDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    merchant = MerchantSerializer()
    category = CategorySerializer()
    address = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField(default=False)


class ConnectionRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    # sender_shop = ShopSerializer(read_only=True)
    receiver_shop_id = serializers.IntegerField(write_only=True)
    receiver_shop = ShopSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        receiver_shop_id = validated_data.get('receiver_shop_id')
        sender_shop_data = Shop.objects.get(active=True)
        status = validated_data.get('status')
        sender_shop = Shop.objects.get(id=sender_shop_data['id'])
        receiver_shop = Shop.objects.get(id=receiver_shop_id)

        return ShopConnection.objects.create(sender_shop=sender_shop, receiver_shop=receiver_shop, status=status)

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        instance.status = status
        instance.save()
        return instance
class ConnectionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    # sender_shop_id = serializers.IntegerField(write_only=True)
    sender_shop = ShopSerializer(read_only=True)
    # receiver_shop_id = serializers.IntegerField(write_only=True)
    # receiver_shop = ShopSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    status = serializers.CharField()

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        instance.status = status
        instance.save()
        return instance

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2, default=200)
    quantity = serializers.IntegerField()
    slug = serializers.SlugField(read_only=True)
    shop = ShopSerializer(read_only=True)
    def create(self, validated_data):

        return Product.objects.create(**validated_data)

class BuyProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField()
    # slug = serializers.SlugField(read_only=True)
    # def create(self,validated_data):
class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title')
    price = serializers.DecimalField(source='product.price', max_digits=8, decimal_places=2)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'quantity']
        


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cart', read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'items']