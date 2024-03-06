from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('type',views.TypeList,basename='type')
router.register('category',views.CategoryList,basename='category')
router.register('restaurant',views.RestaurantList,basename='restaurant')

nested_routers = routers.NestedDefaultRouter(router,'restaurant',lookup='restaurant')
nested_routers.register('products',views.ProductList,basename='restaurant-product')




urlpatterns = [
    path('',include(router.urls)),
    path('',include(nested_routers.urls))
    
    # router.register('product',views.ProductList),
    # router.register('product/<int:pk>',views.GetProduct)
]