from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,CreateModelMixin,DestroyModelMixin
from .models import restaurant,type,Category,Product
from .serializers import RestaurantSerializer,TypeSerializer,ProductSerializer,CategorySerializer,ProductListSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView

# Create your views here.
class RestaurantList(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        queryset = restaurant.objects.all()

        try:
            location = self.request.query_params.get('Location')
            if location :
                queryset = restaurant.objects.filter(Location=location)
            return queryset
        except:
            return queryset
        


class TypeList(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = type.objects.all()
    serializer_class = TypeSerializer

class ProductRestaurantList(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return ProductListSerializer(*args,**kwargs)
        if self.action == 'list':
            return ProductSerializer(*args,**kwargs)

class ProductList(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer

class ProductCategoryList(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.filter(Category_id=self.kwargs['category_pk'])

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return ProductListSerializer(*args,**kwargs)
        if self.action == 'list':
            return ProductSerializer(*args,**kwargs)
          
class RestaurantTypeList(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    serializer_class = RestaurantSerializer
    
    def get_queryset(self):
        return restaurant.objects.filter(type_id=self.kwargs['type_pk'])


class CategoryList(RetrieveModelMixin,GenericViewSet,ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


