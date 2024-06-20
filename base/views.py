from django.db.models import Prefetch
from rest_framework.viewsets import *
from rest_framework.mixins import *
from .models import *
from .serializers import *
# Create your views here.


class TypeList(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = type.objects.all()
    serializer_class = TypeSerializer

class CategoryList(RetrieveModelMixin,GenericViewSet,ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RestaurantList(ModelViewSet):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        queryset = restaurant.objects.select_related('type').all()
        try:
            location = self.request.query_params.get('Location')
            if location :
                queryset = queryset.filter(Location=location)
        except:
            pass
        try:
            type_id = self.kwargs['type_pk']
            queryset = queryset.filter(type_id=type_id)
        except:
            pass

        return queryset



class ProductList(ListModelMixin,RetrieveModelMixin,GenericViewSet):

    def get_queryset(self):
        queryset = Product.objects.select_related('product_cartitem').prefetch_related('image').select_related('restaurant').select_related('Category').all()
        try:
            queryset = queryset.filter(restaurant_id=self.kwargs['restaurant_pk'])
        except:
            pass
        try:
            queryset = queryset.filter(Category_id=self.kwargs['category_pk'])
        except:
            pass
        return queryset     
        
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer

class ProductImageList(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.all().filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {"product_pk":self.kwargs['product_pk']}


class CartView(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemView(ModelViewSet):

    http_method_names = ['get','post','patch','delete']
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk']).all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method in ['PATCH']:
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id":self.kwargs['cart_pk']}