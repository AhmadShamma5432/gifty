from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from .models import *

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['restaurant','Category']
    list_display = ['name','Price','Rate','Price_status','restaurant']
    list_editable = ['Price','Rate']
    list_filter = ['restaurant','Category']
    list_per_page = 20
    list_select_related = ['restaurant']
    search_fields = ['name__istartswith']

    @admin.display(ordering='Price')
    def Price_status(self,Product):
        if Product.Price <= 10:
            return "Low Price"
        elif Product.Price > 10 and Product.Price <= 100 :
            return "Mid Price"
        else:
            return "High Price"


class RateFilter(admin.SimpleListFilter):
    title = 'By Rate'
    parameter_name = 'Rate'
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        low = '<=2'
        mid = '<=4'
        high = '5'
        return [
            (low,'low'),
            (mid,'mid'),
            (high,'high')
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        low = '<=2'
        mid = '<=4'
        if self.value() == low:
            return queryset.filter(Rate__lt=2)
        elif self.value() == mid :
            return queryset.filter(Rate__gte=2,Rate__lt=4)
        else:
            return queryset.filter(Rate__gte=4)
        
@admin.register(restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'Rate', 'Location', 'type_name','num_products']
    list_editable = ['Rate']
    list_select_related = ['type']
    list_filter = ['Location','type',RateFilter]
    search_fields = ['name__istartswith','Location__istartswith']

    def type_name(self, restaurant):
        return restaurant.type.name
    type_name.short_description = 'Restaurant Type'
    
    @admin.display(ordering='num_products')
    def num_products(self, obj):
        return obj.num_products
    num_products.short_description = 'Number of Products'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(num_products=Count('product'))
    

    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer_username','placed_at']

    def customer_username(self,obj:Customer):
        return obj.customer.user.username

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.select_related('customer__user')
    
@admin.register(type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name__istartswith']

@admin.register(Category)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name__istartswith']




