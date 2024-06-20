from .views import * 
from django.urls import include,path 
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('type',TypeList,basename='type')
router.register('category',CategoryList,basename='category')
router.register('restaurant',RestaurantList,basename='restaurant')
router.register('product',ProductList,basename='product')
router.register('cart',CartView,basename='cart')


nested_routers = routers.NestedDefaultRouter(router,'restaurant',lookup='restaurant')
nested_routers.register('products',ProductList,basename='restaurant-product')

nested_category_routers = routers.NestedDefaultRouter(router,'category',lookup='category')
nested_category_routers.register('products',ProductList,basename='category-product')

nested_type_routers = routers.NestedDefaultRouter(router,'type',lookup='type')
nested_type_routers.register('restaurant',RestaurantList,basename='type-restaurant')

nested_image_routers = routers.NestedDefaultRouter(router,'product',lookup='product')
nested_image_routers.register('images',ProductImageList,basename='product-image')

nested_cart_router = routers.NestedDefaultRouter(router,'cart',lookup='cart')
nested_cart_router.register('items',CartItemView,basename='cart-items')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(nested_routers.urls)),
    path('',include(nested_category_routers.urls)),
    path('',include(nested_type_routers.urls)),
    path('',include(nested_image_routers.urls)),
    path('',include(nested_cart_router.urls)),
    
    
]