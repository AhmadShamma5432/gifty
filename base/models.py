from django.db import models
from django.core.validators import MaxValueValidator
############################################################################
VERY_SMALL = 'VS'
SMALL = 'S'
MEDIUM = 'M'
LARGE = 'L'
VERY_LARGE = 'VL'

SIZE_CHOICES = [
    (VERY_SMALL, 'Very Small'),
    (SMALL, 'Small'),
    (MEDIUM, 'Medium'),
    (LARGE, 'Large'),
    (VERY_LARGE, 'Very Large'),
]

# Create your models here.

class type(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)

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


def get_size_display(self):
    return dict(self.SIZE_CHOICES)[self.size]
