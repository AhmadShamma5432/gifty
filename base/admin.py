from django.contrib import admin
from django.utils.html import format_html
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

