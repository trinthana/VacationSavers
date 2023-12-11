from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from app.models import UserProfile

class ChangePasswordForm(PasswordChangeForm):
    # You can add any additional form fields or customization here if needed
    pass

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    # email = forms.
    class Meta:
        model = UserProfile
        fields = ['address', 'postal_code', 'phone', 'image_file', 'subscribed_package', 'subscribed_date', 'expired_date']