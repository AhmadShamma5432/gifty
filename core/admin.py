from django.contrib import admin
from .models import * 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone_number','is_active','is_staff']
    list_filter = ['is_active','is_staff']
    