from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'favorites', FavoriteView, basename='favorite')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'coupons', CouponViewSet, basename='coupons')
# router.register('cart',CartView,basename='cart')


nested_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
nested_router.register(r'products', ProductViewSet, basename='category-products')

# nested_cart_router = routers.NestedDefaultRouter(router,'cart',lookup='cart')
# nested_cart_router.register('items',CartItemView,basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    # path('', include(nested_cart_router.urls)),
    
    
]