from django.db import models
from foodordering.settings import AUTH_USER_MODEL
from .validations import validate_rate, validate_price


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
# class Cart(models.Model):
#     id = models.UUIDField(primary_key=True,default=uuid4)
#     created_at = models.DateField(auto_now_add=True)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
#     product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_cartitem')
#     quantity = models.PositiveIntegerField(validators=[validate_quantity])

#     class Meta:
#         unique_together = [['cart','product']]


# class Order(models.Model):
#     pending = 'P'
#     complete = 'C'
#     failed = 'F'
#     CHOICES_ARRAY = [
#         (pending , 'pending'),
#         (complete , 'complete'),
#         (failed , 'failed')
#     ]
#     placed_at = models.DateField(auto_now_add = True)
#     payment_status = models.CharField( max_length=1,choices = CHOICES_ARRAY , default=pending)
#     customer = models.ForeignKey(Customer,on_delete=models.PROTECT)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name='items')
#     product = models.ForeignKey(Product,on_delete=models.PROTECT)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=9,decimal_places=3)
