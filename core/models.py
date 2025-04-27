from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("The phone field must be set")
        else:
            user = self.model(email=email,**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = models.CharField(max_length=255,unique=False,blank=True,null=True)
    name = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class EmailVerificationCode(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    def __str__(self):
        return f"Code for {self.user.email}"
