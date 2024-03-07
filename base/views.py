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
    queryset = restaurant.objects.all()
    serializer_class = RestaurantSerializer

class TypeList(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = type.objects.all()
    serializer_class = TypeSerializer

class ProductList(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])

    def get_serializer(self, *args, **kwargs):
        try:
            something = self.kwargs['pk']
            return ProductListSerializer(*args,**kwargs)
        except:
            return ProductSerializer(*args,**kwargs)
    

class CategoryList(RetrieveModelMixin,GenericViewSet,ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


