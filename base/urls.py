from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = DefaultRouter()
router.register('type',views.TypeList,basename='type')
router.register('category',views.CategoryList,basename='category')
router.register('restaurant',views.RestaurantList,basename='restaurant')
router.register('product',views.ProductList,basename='restaurant')


nested_routers = routers.NestedDefaultRouter(router,'restaurant',lookup='restaurant')
nested_routers.register('products',views.ProductRestaurantList,basename='restaurant-product')

nested_category_routers = routers.NestedDefaultRouter(router,'category',lookup='category')
nested_category_routers.register('products',views.ProductCategoryList,basename='category-product')

nested_type_routers = routers.NestedDefaultRouter(router,'type',lookup='type')
nested_type_routers.register('restaurant',views.RestaurantTypeList,basename='type-restaurant')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(nested_routers.urls)),
    path('',include(nested_category_routers.urls)),
    path('',include(nested_type_routers.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # router.register('product',views.ProductList),
    # router.register('product/<int:pk>',views.GetProduct)
]