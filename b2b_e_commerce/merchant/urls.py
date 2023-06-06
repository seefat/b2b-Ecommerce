from django.urls import path
from .views import *
urlpatterns = [
    path('merchants/',MerchantViews.as_view(), name='merchant'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='signin'),
    path('categories/',CategoryListView.as_view(),name='category-list'),
    path('create-category/',CategoryCreateView.as_view(),name='category-create'),
    path('shops/',ShopSerializerView.as_view(), name='shops'),
    path('myshops/',MyShopSerializerView.as_view(), name='my-shops'),
    path('my-active-shop/<slug:shop_slug>/',MyActiveShopSerializerView.as_view(), name='my-shop'),
    path('my-active-shop/<slug:shop_slug>/sent-request/',ConnectionRequestCreateView.as_view(), name='sent-request'),
    path('my-active-shop/<slug:shop_slug>/received-requests/',ConnectionReceivedView.as_view(), name='received-requests'),
    path('my-active-shop/<slug:shop_slug>/received-request/<slug:shopconnection_slug>',ConnectionResponseView.as_view(), name='received-requests'),
    path('my-active-shop/<slug:shop_slug>/my-products/',MyProductView.as_view(), name='received-requests'),
    path('my-active-shop/<slug:shop_slug>/same-category/',SameCategoryShop.as_view(), name='same-categories'),
    path('my-active-shop/<slug:shop_slug>/connected-shops/',ConnectedShops.as_view(), name='connected-shops'),
    path('my-active-shop/<slug:shop_slug>/buy-products/',BuyProducts.as_view(), name='buy-products'),
    path('my-active-shop/<slug:shop_slug>/cart/',CartItems.as_view(), name='cart'),
]
