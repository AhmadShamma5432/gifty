from rest_framework import serializers
from django.db import transaction
from .models import *

#Dont forget to add logo
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = type
        fields = ['id','name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','logo']

class RestaurantSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = restaurant
        fields = ['id','name','Rate','Location','type','image']
    
    def get_type(self,obj):
        if( obj.type != None):
            return 1
        else:
            return None
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','image']
        model = ProductImage
    
    def create(self, validated_data):
        product_id = self.context['product_pk']
        return ProductImage.objects.create(product_id=product_id,**validated_data)

class ProductListSerializer(serializers.ModelSerializer):
    # category = serializers.IntegerField()
    # restaurant = serializers.IN()
    # image = ProductImageSerializer(read_only=True,many=True)
    class Meta:
        model = Product
        fields = ['id','name','Rate','Price','Date_of_creation','Descreption','size']

    # def get_restaurant(self,obj):
    #     return obj.restaurant.name

    # def get_category(self,obj):
    #     return obj.Category.name


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField()
    # restaurant = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','Rate','Price','Date_of_creation']

    # def get_restaurant(self,obj):
    #     return obj.restaurant.name

    # def get_category(self,obj):
    #     return obj.Category.name
    


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','Price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

    def get_total_price(self,obj):
        return obj.product.Price * obj.quantity

class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']
    
    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_pk']
        with transaction.atomic():

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"The product you are looking for is not exist")
            
            cart_item , created = CartItem.objects.get_or_create(cart_id=cart_id,
                                                                product=product,
                                                                defaults={'quantity':quantity})
            if not created :
                cart_item.quantity += quantity
                cart_item.save()

            self.instance = cart_item

            return self.instance

class UpdateCartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']
    
    def get_total_price(self,obj):
        return obj.product.Price * obj.quantity

class CreateCartSerailizer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Cart
        fields = ['id','created_at']

class GetCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','items','total_price']

    def get_total_price(self,obj):
        return sum([ value.product.Price * value.quantity for value in obj.items.all()])

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','user_id','phone_number','birth_date']

    def create(self, validated_data):
        user_id = self.context['user_id']
        validated_data['user_id'] = user_id

        cus = Customer.objects.create(**validated_data)
        print(cus)
        return cus

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True,many=True)
    class Meta:
        model = Order
        fields = ['id','placed_at','payment_status','customer','items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializers(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self,value):
        if not Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No cart with given ID was found")
        if CartItem.objects.filter(cart_id = value).count() == 0 :
            raise serializers.ValidationError("The Cart is empty")

    def save(self, **kwargs):

        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

            if len(cart_items) == 0 :
                raise serializers.ValidationError("There is no items in your cart to order")

            customer ,created= Customer.objects.get_or_create(user_id=user_id)
            order = Order.objects.create(customer_id=customer.id)

            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    price = item.product.Price
                )
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order