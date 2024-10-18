from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LoginToken

# Define the admin class
class LoginTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')  # Customize as needed
    search_fields = ('user__username', 'token')  # Enable search by username and token
    list_filter = ('created_at',)  # Filter options in the admin interface

# Register the model with the admin site
admin.site.register(LoginToken, LoginTokenAdmin)