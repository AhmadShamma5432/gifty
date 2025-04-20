from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem
from .models import (
    Category,
    Brand,
    Product,
    CategoryBrand,
    ProductCategory,
    ProductImage,
    Favorite,
    City
)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'image_thumbnail')
    search_fields = ('name_en', 'name_ar')
    list_filter = ('name_en',)
    readonly_fields = ('image_thumbnail',)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = 'Image Preview'

admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id','name_en', 'name_ar', 'address', 'city', 'image_thumbnail')
    search_fields = ('name_en', 'name_ar', 'address', 'city')
    list_filter = ('city',)
    readonly_fields = ('image_thumbnail',)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = 'Image Preview'

admin.site.register(Brand, BrandAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'price', 'rate', 'brand', 'is_active')
    search_fields = ('name_en', 'name_ar')
    list_filter = ('brand', 'is_active')
    inlines = [ProductImageInline, ProductCategoryInline]

admin.site.register(Product, ProductAdmin)

class CategoryBrandAdmin(admin.ModelAdmin):
    list_display = ('category', 'brand', 'created_at')
    list_filter = ('category', 'brand')
    search_fields = ('category__name_en', 'brand__name_en')

admin.site.register(CategoryBrand, CategoryBrandAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'created_at')
    list_filter = ('product', 'category')
    search_fields = ('product__name_en', 'category__name_en')

admin.site.register(ProductCategory, ProductCategoryAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name_en')

admin.site.register(Favorite, FavoriteAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name_en', 'name_ar')
    
    search_fields = ('name_en', 'name_ar')
    
    list_filter = ('name_en',)

admin.site.register(City, CityAdmin)


from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .models import Cart, CartItem, Product

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    autocomplete_fields = ('product',)
    min_num = 1
    max_num = 10


    def total_price_inline(self, obj):
        return obj.quantity * obj.product.price
    total_price_inline.short_description = 'Total Price'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','cart', 'product','quantity', 'total_price')
    search_fields = ('cart__id', 'product__name')
    list_filter = ('cart', 'product')

    def total_price(self, obj):
        return obj.quantity * obj.product.price
    total_price.short_description = 'Total Price'
    total_price.admin_order_field = 'product__price'

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_items', 'total_price')
    search_fields = ('id',)
    list_filter = ('created_at',)
    inlines = [CartItemInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('items')
        queryset = queryset.annotate(
            total_price=Sum(
                ExpressionWrapper(
                    F('items__quantity') * F('items__product__price'),
                    output_field=DecimalField()
                )
            )
        )
        return queryset

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = 'Total Items'

    def total_price(self, obj):
        return obj.total_price or 0
    total_price.short_description = 'Total Price'
    total_price.admin_order_field = 'total_price'


# Register the models with the admin site
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)