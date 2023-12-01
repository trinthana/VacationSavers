from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile

class ChangePasswordForm(PasswordChangeForm):
    # You can add any additional form fields or customization here if needed
    pass

class UserProfileForm(forms.ModelForm):
    # email = forms.
    class Meta:
        model = UserProfile
        fields = ['phone', 'website', 'address', 'zipcode']