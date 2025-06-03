from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from app.campaigner_email import send_password_reset_email  # We'll define this next
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}),
  )
  password2 = forms.CharField(
      label=_("Password Confirmation"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Confirm Password"}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          "placeholder": "Username",
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          "placeholder": "Email"
      })
    }

class RegistrationWithCodeForm(UserCreationForm):
  token = forms.CharField(
      label=_("Token"),
      widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Token", "required": True, 'readonly': 'readonly'}),
  )
  password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}),
  )
  password2 = forms.CharField(
      label=_("Password Confirmation"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Confirm Password"}),
  )

  class Meta:
    model = User
    fields = ('username', 'email')

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          "placeholder": "Username",
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          "placeholder": "Email"
      }),
    }
       

class LoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label=_("Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        "placeholder": "Email",
    }))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "New Password",
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Confirm New Password"
    }), label="Confirm New Password")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Current Password"
    }), label='Current Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "New Password"
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Confirm New Password"
    }), label="Confirm New Password")


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'id': 'id_email'
        })
    )

    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False,
             token_generator=None,
             from_email=None,
             request=None,
             html_email_template_name=None,
             extra_email_context=None):

        # Default to Django's token generator if not provided
        if not token_generator:
            from django.contrib.auth.tokens import default_token_generator
            token_generator = default_token_generator

        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        email = self.cleaned_data["email"]
        users = list(self.get_users(email))  # Cast to list to avoid multiple iterations

        if not users:
            return  # Do nothing if no user found

        user = users[0]  # Only use the first user

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"https://{request.get_host()}/accounts/password-reset-confirm/{uid}/{token}/"

        print(f"Sending password reset email to: {user.email}")
        send_password_reset_email(
            email=user.email,
            first_name=user.first_name,
            reset_link=reset_url
        )