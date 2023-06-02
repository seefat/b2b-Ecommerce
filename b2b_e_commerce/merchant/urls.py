from django.urls import path
from .views import *
urlpatterns = [
    path('all/',MerchantViews.as_view(), name='merchant'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='signin'),
    path('categories/',CategoryListView.as_view(),name='category-list'),
    path('category/create/',CategoryCreateView.as_view(),name='category-create'),
    path('shop/',ShopSerializerView.as_view(), name='shop'),
    path('myshops/',MyShopSerializerView.as_view(), name='my-shops'),
    path('myshops/<slug:shop_id>/',MyActiveShopSerializerView.as_view(), name='my-shop'),
    path('myshops/<int:shop_id>/sent-request/',ConnectionRequestCreateView.as_view(), name='sent-request'),
    path('myshops/<int:shop_id>/received-requests/',ConnectionReceivedView.as_view(), name='received-requests'),
    path('myshops/<int:shop_id>/received-request/<int:shopconnection_id>',ConnectionResponseView.as_view(), name='received-requests'),
]
