from django.db import models
from uuid import uuid4
from .validations import * 
############################################################################

# Create your models here.

class type(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(blank=True,null=True,upload_to='base/category_logos')


class restaurant(models.Model):
    name = models.TextField()
    Rate = models.DecimalField(max_digits=4,decimal_places=2,validators=[validate_rate])
    Location = models.CharField(max_length=255)
    type = models.ForeignKey(type,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to='base/restaurant_images')

class Product(models.Model):
    name = models.CharField(max_length=255)
    Rate = models.DecimalField(max_digits=4,decimal_places=2,validators=[validate_rate],null=True)
    Price = models.DecimalField(max_digits=19,decimal_places=9,validators=[validate_price])
    Date_of_creation= models.DateField(auto_now_add=True)
    restaurant = models.ForeignKey(restaurant,on_delete=models.SET_NULL,null=True)
    Category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    Descreption = models.TextField()
    size = models.CharField(max_length=50,default='Small',null=True,blank=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,related_name='image')
    image = models.ImageField(upload_to='base/product_images')


class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_cartitem')
    quantity = models.PositiveIntegerField(validators=[validate_quantity])

    class Meta:
        unique_together = [['cart','product']]