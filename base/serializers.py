from rest_framework import serializers
from .models import restaurant,type,Category,Product

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = type
        fields = ['id','name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class RestaurantSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    class Meta:
        model = restaurant
        fields = ['id','name','Rate','Location','type','image']

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = restaurant
        fields = ['name']

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='Category')
    class Meta:
        model = Product
        fields = ['id','name','restaurant','Rate','Price','Date_of_creation','Descreption','sizes','category','images']
    restaurant = SimpleRestaurantSerializer()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='Category')
    class Meta:
        model = Product
        fields = ['id','name','restaurant','Rate','Price','Date_of_creation','category']
    restaurant = SimpleRestaurantSerializer()
        
    
        
