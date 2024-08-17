from django.db.models import Prefetch
from rest_framework.viewsets import *
from rest_framework.mixins import *
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .models import *
from .serializers import *
# Create your views here.


class TypeList(RetrieveModelMixin,ListModelMixin,GenericViewSet):
    queryset = type.objects.all()
    serializer_class = TypeSerializer

class CategoryList(UpdateModelMixin,CreateModelMixin,RetrieveModelMixin,ListModelMixin,GenericViewSet):
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

class ProductList(UpdateModelMixin,ListModelMixin,RetrieveModelMixin,GenericViewSet):

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('image').select_related('restaurant').select_related('Category').all()
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
        else:
            return ProductSerializer

class ProductImageList(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.all().filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {"product_pk":self.kwargs['product_pk']}

class CartView(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartSerailizer
        elif self.request.method == 'GET':
            return GetCartSerializer

class CartItemView(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return UpdateCartItemSerializer
        elif self.request.method == 'POST':
            return CreateCartItemSerializer
        else:
            return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_pk":self.kwargs['cart_pk']}
    
class CustomerView(CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,GenericViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(user_id=self.request.user.id)

    def get_serializer_context(self):
        return {"user_id":self.request.user.id}
    

    def perform_create(self, serializer):
        return serializer.save()
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = self.perform_create(serializer)
        return Response(CustomerSerializer(customer).data)
    
    
    @action(detail=False,methods=['GET','PUT'])
    def me(self,request):
        customer , created = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderView(DestroyModelMixin,ListModelMixin,RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,GenericViewSet):
    
    http_method_names = ['patch','delete','options','head','get','post']
    def get_permissions(self):

        if self.request.method in ['PATCH','DELETE','OPTIONS','HEAD']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializers
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        else:
            customer , created = Customer.objects.get_or_create(user_id=self.request.user.id)
            return Order.objects.prefetch_related('items__product').filter(customer=customer)
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializers(data=request.data,context={"user_id":self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(OrderSerializer(order).data)
    