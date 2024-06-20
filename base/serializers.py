from rest_framework import serializers
from .models import *
from pprint import pprint

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
        return obj.type.name
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','image']
        model = ProductImage
    
    def create(self, validated_data):
        product_id = self.context['product_pk']
        return ProductImage.objects.create(product_id=product_id,**validated_data)

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    image = ProductImageSerializer(read_only=True,many=True)
    class Meta:
        model = Product
        fields = ['id','name','restaurant','Rate','Price','Date_of_creation','Descreption','size','category','image']

    def get_restaurant(self,obj):
        return obj.restaurant.name

    def get_category(self,obj):
        return obj.Category.name


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name','restaurant','Rate','Price','Date_of_creation','category']

    def get_restaurant(self,obj):
        return obj.restaurant.name

    def get_category(self,obj):
        return obj.Category.name
    


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

class CartSerializer(serializers.ModelSerializer):
    id =  serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True,many=True)
    total_price = serializers.SerializerMethodField() 
    class Meta:
        model = Cart
        fields = ['id','items','total_price']

    def get_total_price(self,obj):
        return sum([value.product.Price * value.quantity for value in obj.items.all()])
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("The product with the given ID is not exist")
        else:
            return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        
        try:
            cart_item = CartItem.objects.get(product_id=product_id,cart_id=cart_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data) 
        return self.instance
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']