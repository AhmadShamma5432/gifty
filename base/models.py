from django.db import models
from django.core.validators import MaxValueValidator
############################################################################

# Create your models here.

class type(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    # logo = models.URLField()
    # logos = models.URLField()


class restaurant(models.Model):
    name = models.TextField()
    Rate = models.DecimalField(max_digits=3,decimal_places=2)
    Location = models.CharField(max_length=255)
    type = models.ForeignKey(type,on_delete=models.SET_NULL,null=True)
    image = models.URLField()

class Product(models.Model):
    name = models.CharField(max_length=255)
    Rate = models.DecimalField(max_digits=3,decimal_places=2)
    Price = models.DecimalField(max_digits=19,decimal_places=9)
    Date_of_creation= models.DateField(auto_now_add=True)
    restaurant = models.ForeignKey(restaurant,on_delete=models.SET_NULL,null=True)
    Category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    Descreption = models.TextField()
    size = models.CharField(max_length=50,default='Small')
    images = models.TextField()

