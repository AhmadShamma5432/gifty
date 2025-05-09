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
    images = serializers.SerializerMethodField()
    # images = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for product images
    brand = BrandSerializer(read_only=True)
    favorite_id = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'name_en', 'name_ar', 'description_en',
            'description_ar','preparing_time',
            'rate', 'price', 'date_of_creation', 'brand', 'is_active', 'images','favorite_id'
        ]

    def get_images(self,obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        
    
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
    product = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = ProductCategory
        fields = ['product']  

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
    

class OrderItemProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    # images = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for product images
    brand = BrandSerializer(read_only=True)
    # favorite_id = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'name_en', 'name_ar', 'description_en',
            'description_ar','preparing_time',
            'rate', 'price', 'date_of_creation', 'brand', 'is_active', 'images'
        ]

    def get_images(self,obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product','product_id', 'quantity', 'notes', 'total_product_price']


class CouponSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Coupon
        fields = [ 'id', 'code', 'discount_percentage', 'valid_from', 'valid_to',
                    'user', 'is_active','coupon_type']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UserSerializer(read_only=True)
    coupon = CouponSerializer(read_only=True)
    coupon_id = serializers.IntegerField(write_only=True,required=False)

    class Meta:
        model = Order
        fields = ['id', 'payment_status', 'placed_at', 'location1', 'location2', 'phone1', 'phone2' ,'coupon','coupon_id', 'delievery_time','delievery_price', 'total_products_price', 'user', 'items']

    def create(self, validated_data):
        with transaction.atomic():
            user_id = self.context['user_id']
            user = self.context['user']
            
            items_data = validated_data.pop('items')

            coupon = None

            try:
                coupon_id = validated_data['coupon_id']
            except:
                coupon_id = None
            if coupon_id:
                try:
                    coupon = Coupon.objects.get(pk=coupon_id)
                except Coupon.DoesNotExist:
                    raise serializers.ValidationError({"message": "Invalid coupon."})

                if not coupon.is_valid(user=user):
                    raise serializers.ValidationError({"message": "This coupon is not valid for you."})
                
                if UsedCoupons.objects.filter(user=user,coupon=coupon):
                    raise serializers.ValidationError({"message": "you already have used this coupon"})
                
                UsedCoupons.objects.create(user=user,coupon=coupon)
            user_orders = Order.objects.filter(user_id=user_id,payment_status__in=['A'])
            # user_orders = Order.objects.filter(user_id=user_id,payment_status__in=['A','P'])

            if user_orders.exists():
                raise ValidationError("You already have a pending order. Please wait until it is completed before placing a new one.")

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
        