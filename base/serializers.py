from rest_framework import serializers
from .models import Category, Brand, Product, CategoryBrand, ProductCategory, ProductImage
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import *
from core.serializers import UserSerializer

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
    favorite_id = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'name_en', 'name_ar', 'description_en',
            'description_ar','preparing_time',
            'rate', 'price', 'date_of_creation', 'brand', 'is_active', 'images','favorite_id'
        ]

    def get_favorite_id(self,obj):
        if len(obj.user_favorites) == 0:
            return None 
        return obj.user_favorites[0].id
    
class FavoriteProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for product images
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class CategoryBrandSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  
    brand = serializers.StringRelatedField()     

    class Meta:
        model = CategoryBrand
        fields = ['id', 'category', 'brand', 'created_at']

class ProductListFromCategorySerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = ProductCategory
        fields = ['product']  

    def get_product(self, obj):
        brand = BrandSerializer(obj.product.brand)
        images = ProductImageSerializer(obj.product.images.all(), many=True).data
        return {
            "id": obj.product.id,
            "name_en": obj.product.name_en,
            "name_ar": obj.product.name_ar,
            "description_en": obj.product.description_en,
            "description_ar": obj.product.description_ar,
            "preparing_time": obj.product.preparing_time,
            "rate": str(obj.product.rate),  
            "price": str(obj.product.price),
            "date_of_creation": obj.product.date_of_creation,
            "brand": brand.data,
            "is_active": obj.product.is_active,
            "images": images
        }
    
class FavoriteSerializer(serializers.ModelSerializer):
    product = FavoriteProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Favorite
        fields = ['id','product','product_id']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        user_id = self.context['user_id']

        return Favorite.objects.create(product_id=product_id,user_id=user_id)
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product','product_id', 'quantity', 'notes', 'total_product_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'payment_status', 'placed_at', 'location1', 'location2', 'phone1', 'phone2', 'delievery_time','delievery_price', 'total_products_price', 'user', 'items']

    def create(self, validated_data):
        user_id = self.context['user_id']
        items_data = validated_data.pop('items')

        user_orders = Order.objects.filter(user_id=user_id,payment_status__in=['A'])
        print(user_orders)
        if user_orders.exists():
            raise ValidationError("You already have a pending order. Please wait until it is completed before placing a new one.")

        with transaction.atomic():
            order = Order.objects.create(user_id=user_id, **validated_data)

            # Bulk create order items
            order_items = [
                OrderItem(order=order, **item_data) for item_data in items_data
            ]
            OrderItem.objects.bulk_create(order_items)
            order = Order.objects.prefetch_related('items__product__images')\
                                .prefetch_related('items__product__brand__city')\
                                .select_related('user').get(id=order.id)
            return order