from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,phone,password=None,**extra_fields):
        if not phone:
            raise ValueError("The phone field must be set")
        else:
            user = self.model(phone=phone,**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)
    
class User(AbstractUser):
    username = models.CharField(max_length=255,unique=False,blank=True,null=True)
    name = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True,max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []