from django.db import models
from uuid import uuid4
from foodordering.settings import AUTH_USER_MODEL
from .validations import validate_rate, validate_price,validate_quantity


class Category(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    description_en = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return f"{self.name_en} "

    class Meta:
        db_table = 'category'

class City(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name_en}"

    class Meta:
        db_table = 'city'        

class Brand(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    description_en = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="brands")
    image = models.ImageField(upload_to='brands/', null=True, blank=True)

    def __str__(self):
        return f"{self.name_en}"

    class Meta:
        db_table = 'brand'

class Product(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    description_en = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    preparing_time = models.IntegerField()
    rate = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_rate], null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    date_of_creation = models.DateField(auto_now_add=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, related_name="products")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name_en}"

    class Meta:
        db_table = 'product'

class CategoryBrand(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="brand_relationships")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="category_relationships")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('category', 'brand')
        db_table = 'category_brand'

    def __str__(self):
        return f"{self.category.name_en} - {self.brand.name_en}"

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="category_relationships")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_relationships")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'category')
        db_table = 'product_category'

    def __str__(self):
        return f"{self.product.name_en} - {self.category.name_en}"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)  # Mark one image as primary

    def __str__(self):
        return f"Image for {self.product}"

class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites_product")
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_favorites')

    class Meta:
        unique_together = ('product','user')
        db_table = 'favorite'

class Order(models.Model):
    pending = 'P'
    complete = 'C'
    accepted = 'A'
    failed = 'F'
    CHOICES_ARRAY = [
        (pending , 'pending'),
        (complete , 'complete'),
        (accepted , 'accepted'),
        (failed , 'failed')
    ]
    payment_status = models.CharField( max_length=1,choices = CHOICES_ARRAY , default=pending)
    placed_at = models.DateField(auto_now_add = True)
    location1 = models.TextField()
    location2 = models.TextField()
    phone1 = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255)
    delievery_price = models.IntegerField()
    delievery_time = models.DateTimeField()
    total_products_price = models.DecimalField(max_digits=12,decimal_places=3)
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.IntegerField()
    total_product_price = models.DecimalField(max_digits=12,decimal_places=3)
    notes = models.TextField(blank=True,null=True)

class delieveryTime(models.Model):
    begin_time = models.TimeField()
    end_time = models.TimeField()
    
