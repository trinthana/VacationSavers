from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import UserProfile, SubscriptionHistory, ApplicationToken, PackageChoices
from app.campaigner_email import send_welcome_email
from django.utils import timezone
from datetime import timedelta
import random
import string
import traceback

class BaseUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(write_only=True, allow_blank=True, required=False)
    city = serializers.CharField(write_only=True)
    state_code = serializers.CharField(write_only=True, required=False, allow_blank=True, help_text="2 digits state code")
    postal_code = serializers.CharField(write_only=True)
    country_code = serializers.CharField(write_only=True, help_text="2 digits country code")
    phone = serializers.CharField(write_only=True)
    addon_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    subscribed_date = serializers.DateField(write_only=True, required=False, default=timezone.now)

    def create_user(self, validated_data):
        try:
            # Username fallback to email if not provided
            username = validated_data.get('username') or validated_data.get('email')
            email = validated_data.get('email')
            if not username:
                raise serializers.ValidationError({"username": "Username or email must be provided."})

            if not email:
                raise serializers.ValidationError({"email": "Email is required."})

            # Generate random password
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            token = self.context.get('token')

            # Set subscribed_package (default to PREMIER if not given)
            subscribed_package = validated_data.get('addon_code') or str(PackageChoices.PREMIER)

            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=password
            )

            # Combine phone parts
            phone = f"+{validated_data.get('phone_country', '')}-{validated_data.get('phone_area', '')}-{validated_data.get('phone_number', '')}"

            # Check if a UserProfile already exists
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Update or set fields
            user_profile.address = validated_data.get('address', '')
            user_profile.city = validated_data.get('city', '')
            user_profile.state_code = validated_data.get('state_code', '')
            user_profile.country_code = validated_data.get('country_code', '')
            user_profile.postal_code = validated_data.get('postal_code', '')
            user_profile.phone = validated_data.get('phone', '')
            user_profile.subscribed_package = subscribed_package
            user_profile.subscribed_date = validated_data.get('subscribed_date', timezone.now())
            user_profile.expired_date = validated_data.get('expired_date', timezone.now() + timedelta(days=365))
            user_profile.updated_datetime = timezone.now()
            user_profile.token = token

            user_profile.save()

            # Send Welcome Email
            send_welcome_email(user.email, f"{user.first_name} {user.last_name}", username, password)

            return user

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError({"error": f"Failed to create user: {str(e)}"})
      
class UserSerializer(BaseUserSerializer):
    def create(self, validated_data):
        return self.create_user(validated_data)

class SubscriptionSerializer(BaseUserSerializer):
    phone_country = serializers.CharField()
    phone_area = serializers.CharField()
    phone_number = serializers.CharField()
    cc_number = serializers.CharField(write_only=True)
    cc_exp = serializers.CharField(write_only=True)
    cc_cvv = serializers.CharField(write_only=True)
    locator = serializers.CharField()

    def validate(self, data):
        data['phone'] = f"+{data['phone_country']}-{data['phone_area']}-{data['phone_number']}"
        return data

    def create(self, validated_data):
        user = self.create_user(validated_data)

        subscribed_package = validated_data.get('addon_code') or str(PackageChoices.PREMIER)
        cc_masked = f"**** **** **** {validated_data['cc_number'][-4:]}"
        exp_masked = "**/**"
        cvv_masked = "***"

        ApplicationToken.objects.create(
            user=user,
            application='SUBSCRIPTION',
            token=cc_masked,
            custom1=exp_masked,
            custom2=cvv_masked,
            custom3=validated_data['locator']
        )

        # Save subscription history
        SubscriptionHistory.objects.create(
            user=user,
            subscribed_package=subscribed_package,
            subscribed_date=validated_data.get('subscribed_date', timezone.now())
        )

        # Masked credit card info
        cc_number = validated_data.get('cc_number', '')
        cc_masked = f"**** **** **** {cc_number[-4:]}" if cc_number else ""
        exp_masked = "**/**"
        cvv_masked = "***"

        # Save to ApplicationToken
        ApplicationToken.objects.create(
            user=user,
            application='SUBSCRIPTION',
            token=cc_masked,
            custom1=exp_masked,
            custom2=cvv_masked,
            custom3=validated_data.get('locator', '')
        )

        return user

class UserTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='userprofile.token')

    class Meta:
        model = User
        fields = ('username', 'email', 'token')

class ResponseUserSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)
    token = serializers.CharField(allow_blank=True, required=False)

class RequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

class ResponseSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=True, required=False)

class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(allow_blank=True, required=False)
