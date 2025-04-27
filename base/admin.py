from django.contrib import admin
from django.utils.html import format_html
from .models import * 

class DeliveryTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'begin_time', 'end_time')  # Fields to display in the list view
    search_fields = ('begin_time', 'end_time')       # Enable searching by time fields
    list_filter = ('begin_time', 'end_time')         # Add filters for common fields

# Register the DeliveryTime model with the custom admin class
admin.site.register(delieveryTime, DeliveryTimeAdmin)

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


class OrderItemInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = OrderItem
    extra = 0  # Do not display extra empty forms by default
    readonly_fields = ('total_product_price',)  # Make calculated fields read-only

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'payment_status',
        'placed_at',
        'total_products_price',
        'delivery_time',
    )
    list_filter = ('payment_status', 'placed_at')  # Add filters for common fields
    search_fields = ('user__username', 'id')  # Enable searching by user or order ID
    readonly_fields = ('placed_at', 'total_products_price')  # Protect calculated/automatic fields
    inlines = [OrderItemInline]  # Include the inline for OrderItem

    def delivery_time(self, obj):
        return obj.delievery_time  # Display the delivery time field
    delivery_time.short_description = 'Delivery Time'