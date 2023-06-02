from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.settings import api_settings
from rest_framework.response import Response
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors ,status.HTTP_400_BAD_REQUEST)
# class CreateTokenView(TokenObtainPairView):
#     def post(self, request):
#         serializer = TokenObtainPairSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status.HTTP_201_CREATED)
#         return Response(serializer.errors ,status.HTTP_400_BAD_REQUEST)
class MerchantViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_merchants = Merchant.objects.all()
        serializer = MerchantSerializer(all_merchants, many=True)
        return Response(serializer.data)
    @extend_schema(
        request=UserSerializer, # Serializer used for the request body
        responses={201: UserSerializer}, # Serializer used for the response body
    )
    def post(self, request):
        serializer = MerchantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            merchant = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=UserSerializer, # Serializer used for the request body
        responses={201: UserSerializer}, # Serializer used for the response body
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            response_data = {
                'user_id': user.id,
                'email': user.email,
                'tokens': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopSerializerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_shops = Shop.objects.all()
        serializer = ShopSerializer(all_shops, many=True)
        return Response(serializer.data)

    # @extend_schema(
    #     request=ShopSerializer,
    #     responses={201: ShopSerializer},
    # )
    # def post(self,request):
    #     serializer = ShopSerializer(data=request.data,context={'request': request})
    #     if serializer.is_valid():
    #         shop = serializer.save()
    #         return Response(serializer.data, status.HTTP_201_CREATED)
    #     return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class MyShopSerializerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        merchant = request.user.merchant
        my_shops = Shop.objects.filter(merchant=merchant)
        serializer = ShopSerializer(my_shops, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ShopSerializer,
        responses={201: ShopSerializer},
    )
    # def post(self,request):
    #     serializer = ShopSerializer(data=request.data,context={'request': request})
    #     if serializer.is_valid():
    #         shop = serializer.save()
    #         return Response(serializer.data, status.HTTP_201_CREATED)
    #     return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        merchant = request.user.merchant
        my_shops = Shop.objects.filter(merchant=merchant)
        my_shops.update(active=False)   # Deactivating all the merchant's shops

        serializer = ShopSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            shop = serializer.save()
            shop.active = True  # Activating the newly created shop
            shop.save()

            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class MyActiveShopSerializerView(APIView):
    def get(self, request, shop_id):
        merchant = request.user.merchant
        my_shops = Shop.objects.filter(merchant=merchant)
        my_shops.update(active=False)   # Deactivating all the merchant's shops
        shop = Shop.objects.get(id=shop_id)
        shop.active=True    #activating my specific shop
        serializer = MyShopDetailSerializer(shop)
        return Response(serializer.data)


class LoginView(APIView):
    @extend_schema(
        request=ShopSerializer, # Serializer used for the request body
        responses={201: ShopSerializer}, # Serializer used for the response body
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request=request, username=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)

                response_data = {
                    'user_id': user.id,
                    'email': user.email,
                    'tokens': {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                    }
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'error': 'Invalid credentials'
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConnectionRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ShopSerializer, # Serializer used for the request body
        responses={201: ShopSerializer}, # Serializer used for the response body
    )

    def get(self, request, shop_id):
        # merchant = request.user.merchant
        # my_shops = Shop.objects.filter(merchant=merchant)
        # my_shops.update(active=False)   # Deactivating all the merchant's shops
        # shop = Shop.objects.get(id=shop_id)
        # shop.active=True
        # shop.save()
        # sender_shop = Shop.objects.filter(merchant=merchant,active=True,)
        # sender_shop = ShopConnection.objects.get(sender_shop_id=shop_id)
        sender_shop = get_object_or_404(Shop, id=shop_id)
        sender_shop.active=True
        sender_shop.save()
        query = ShopConnection.objects.filter(sender_shop=sender_shop) #.values_list('receiver_shop', flat=True)

        serializer = ConnectionRequestSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, shop_id):
        serializer = ConnectionRequestSerializer(data=request.data)
        if serializer.is_valid():
            receiver_shop_id = serializer.validated_data.get('receiver_shop_id')
            sender_shop = get_object_or_404(Shop, id=shop_id)
            # status = serializer.validated_data.get('status')
            receiver_shop = Shop.objects.get(id=receiver_shop_id)

            connection = ShopConnection.objects.create(
                sender_shop=sender_shop,
                receiver_shop=receiver_shop,
                status='pending'
            )

            res = ConnectionRequestSerializer(connection)
            return Response(res.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConnectionReceivedView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ConnectionResponseSerializer, # Serializer used for the request body
        responses={201: ShopSerializer}, # Serializer used for the response body
    )

    def get(self, request, shop_id):

        receiver_shop = get_object_or_404(Shop, id=shop_id)
        receiver_shop.active=True
        receiver_shop.save()
        query = ShopConnection.objects.filter(receiver_shop=receiver_shop) #.values_list('receiver_shop', flat=True)

        serializer = ConnectionResponseSerializer(query, many=True)
        return Response(serializer.data)

    # def patch(self, request, shop_id):
    #     serializer = ConnectionResponseSerializer(data=request.data)
    #     if serializer.is_valid():
    #         receiver_shop_id = serializer.validated_data.get('receiver_shop_id')
    #         sender_shop = get_object_or_404(Shop, id=shop_id)
    #         # status = serializer.validated_data.get('status')
    #         receiver_shop = Shop.objects.get(id=receiver_shop_id)

    #         connection = ShopConnection.objects.create(
    #             sender_shop=sender_shop,
    #             receiver_shop=receiver_shop,
    #             status='pending'
    #         )

    #         res = ConnectionResponseSerializer(connection)
    #         return Response(res.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConnectionResponseView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ConnectionResponseSerializer, # Serializer used for the request body
        responses={201: ShopSerializer}, # Serializer used for the response body
    )

    def get(self, request, shop_id, shopconnection_id):

        receiver_shop = get_object_or_404(Shop, id=shop_id)
        receiver_shop.active=True
        receiver_shop.save()
        query = ShopConnection.objects.filter(id=shopconnection_id) #.values_list('receiver_shop', flat=True)

        serializer = ConnectionResponseSerializer(query, many=True)
        return Response(serializer.data)

    def patch(self, request, shop_id, shopconnection_id):
        receiver_shop = get_object_or_404(Shop, id=shop_id)
        receiver_shop.active = True
        receiver_shop.save()

        shop_connection = get_object_or_404(ShopConnection, id=shopconnection_id, receiver_shop=receiver_shop)

        serializer = ConnectionResponseSerializer(shop_connection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('status') == 'approved':
            sender_shop = shop_connection.sender_shop

            # Create a new connection with reversed sender and receiver
            ShopConnection.objects.create(sender_shop=receiver_shop, receiver_shop=sender_shop, status='approved')

        elif serializer.validated_data.get('status') == 'declined':
            # Delete the connection
            shop_connection.delete()
        serializer.save()

        return Response(serializer.data)


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]
    @extend_schema(
        request=CategorySerializer, # Serializer used for the request body
        responses={201: CategorySerializer}, # Serializer used for the response body
    )

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
