from rest_framework import serializers
from .models import Category, Brand, Product, CategoryBrand, ProductCategory, ProductImage
from rest_framework import serializers
from django.db import transaction
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_en', 'name_ar', 'description_en', 'description_ar', 'image']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name_en', 'name_ar']

class BrandSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    class Meta:
        model = Brand
        fields = ['id', 'name_en', 'name_ar', 'description_en', 'description_ar', 'address', 'city', 'image']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'is_primary']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for product images
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Product
        fields = [
            'id', 'name_en', 'name_ar', 'description_en', 'description_ar',
            'rate', 'price', 'date_of_creation', 'brand', 'is_active', 'images'
        ]

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name_en','name_ar','price']

class CategoryBrandSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  
    brand = serializers.StringRelatedField()     

    class Meta:
        model = CategoryBrand
        fields = ['id', 'category', 'brand', 'created_at']

class ProductListFromCategorySerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = ProductCategory
        fields = ['product','image']  

    def get_product(self, obj):
        brand = BrandSerializer(obj.product.brand)
        return {
            "id": obj.product.id,
            "name_en": obj.product.name_en,
            "name_ar": obj.product.name_ar,
            "description_en": obj.product.description_en,
            "description_ar": obj.product.description_ar,
            "rate": str(obj.product.rate),  
            "price": str(obj.product.price),
            "date_of_creation": obj.product.date_of_creation,
            "brand": brand.data,
            "is_active": obj.product.is_active
        }
    

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Favorite
        fields = ['id','product','product_id']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        user_id = self.context['user_id']

        return Favorite.objects.create(product_id=product_id,user_id=user_id)

    
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

    def get_total_price(self,obj):
        return obj.product.price * obj.quantity

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
        return obj.product.price * obj.quantity

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
        return sum([ value.product.price * value.quantity for value in obj.items.all()])

# class OrderItemSerializer(serializers.ModelSerializer):
#     product = SimpleProductSerializer()
#     class Meta:
#         model = OrderItem
#         fields = ['id','product','quantity','price']


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(read_only=True,many=True)
#     class Meta:
#         model = Order
#         fields = ['id','placed_at','payment_status','customer','items']

# class UpdateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['payment_status']


# class CreateOrderSerializers(serializers.Serializer):
#     cart_id = serializers.UUIDField()

#     def validate_cart_id(self,value):
#         if not Cart.objects.filter(pk=value).exists():
#             raise serializers.ValidationError("No cart with given ID was found")
#         if CartItem.objects.filter(cart_id = value).count() == 0 :
#             raise serializers.ValidationError("The Cart is empty")

#     def save(self, **kwargs):

#         with transaction.atomic():
#             cart_id = self.validated_data['cart_id']
#             user_id = self.context['user_id']

#             cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

#             if len(cart_items) == 0 :
#                 raise serializers.ValidationError("There is no items in your cart to order")

#             customer ,created= Customer.objects.get_or_create(user_id=user_id)
#             order = Order.objects.create(customer_id=customer.id)

#             order_items = [
#                 OrderItem(
#                     order = order,
#                     product = item.product,
#                     quantity = item.quantity,
#                     price = item.product.price
#                 )
#                 for item in cart_items
#             ]

#             OrderItem.objects.bulk_create(order_items)

#             Cart.objects.filter(pk=cart_id).delete()

#             return order