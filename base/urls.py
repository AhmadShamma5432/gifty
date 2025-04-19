from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'favorites', FavoriteView, basename='favorite')
router.register(r'cities', CityViewSet, basename='city')


nested_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
nested_router.register(r'products', ProductCategoryViewSet, basename='category-products')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    
]