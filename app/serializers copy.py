# serializers.py

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime, timedelta
from rest_framework import serializers
from app.models import UserProfile, PackageChoices, SubscriptionHistory, ApplicationToken
import random
import string

def default_expiry():
    return now().date() + timedelta(days=365)

  
class UserSerializer(serializers.ModelSerializer):
    # Add additional fields for UserProfile
    first_name          = serializers.CharField(write_only=True, allow_blank=True, required=False)
    last_name           = serializers.CharField(write_only=True, allow_blank=True, required=False)
    address             = serializers.CharField(write_only=True, allow_blank=True, required=False)
    city                = serializers.CharField(write_only=True, allow_blank=True, required=False)
    state_code          = serializers.CharField(write_only=True, allow_blank=True, required=False)
    country_code        = serializers.CharField(write_only=True, allow_blank=True, required=False)
    postal_code         = serializers.CharField(write_only=True, allow_blank=True, required=False)
    phone               = serializers.CharField(write_only=True, allow_blank=True, required=False)
    subscribed_package  = serializers.CharField(write_only=True, allow_blank=True, required=False, default=PackageChoices.PREMIER)
    token               = serializers.CharField(write_only=True, allow_blank=True, required=False)
    subscribed_date     = serializers.DateField(write_only=True, required=False, default=timezone.now())
    expired_date        = serializers.DateField(default=default_expiry)
    updated_datetime    = serializers.DateTimeField(write_only=True, default=timezone.now())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'city', 'state_code', 'country_code', 'postal_code', 'phone', 'subscribed_package', 'token', 'subscribed_date', 'expired_date', 'updated_datetime']
   
    def create(self, validated_data):
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        token = self.context.get('token')
        subscribed_package = str(PackageChoices.PREMIER)

         # Create the User object with the generated password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=password
        )

        # Set the subscribed_package to "ABC" if it's not provided
        profile_data = {
            'subscribed_package': subscribed_package,
            'token': token,
            'subscribed_date': validated_data.get('subscribed_date', timezone.now()),
            'expired_date': validated_data.get('expired_date', timezone.now() + timedelta(days=365)),
            'updated_datetime': validated_data.get('updated_datetime', timezone.now()),
            **{field: validated_data.get(field, '') for field in ['address', 'city', 'state_code', 'country_code', 'postal_code', 'phone']}
        }

        # Create the UserProfile object
        try:
            # Attempt to fetch the existing UserProfile
            user_profile = UserProfile.objects.get(user=user)
            # Update the existing UserProfile with the new data
            for key, value in profile_data.items():
                setattr(user_profile, key, value)
            user_profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user, **profile_data)
        except Exception as e:
            print(f"Error creating/updating UserProfile: {e}")
            raise e

        return user

class UserTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='userprofile.token')

    class Meta:
        model = User
        fields = ('username', 'email', 'token')

class CreateUserSerializer(serializers.ModelSerializer):
    # Add additional fields for UserProfile
    username            = serializers.CharField(required=True, help_text="Username must be unique. Using your organization entity as prefix (ENTITY_abcdefg) is recommended.")
    first_name          = serializers.CharField(required=True)
    last_name           = serializers.CharField(required=True)
    email               = serializers.CharField(required=True)
    address             = serializers.CharField(required=True)
    city                = serializers.CharField(required=True)
    state_code          = serializers.CharField(allow_blank=True, required=False, help_text="2 digits state code")
    country_code        = serializers.CharField(required=True, help_text="2 digits country code")
    postal_code         = serializers.CharField(allow_blank=True, required=False)
    phone               = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'city', 'state_code', 'country_code', 'postal_code', 'phone']

class ResponseUserSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)
    token = serializers.CharField(allow_blank=True, required=False, help_text="Token will be returned")


class RequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="Username must be unique. Using your organization entity as prefix (ENTITY_abcdefg) is recommended.")


class ResponseSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=True, required=False, help_text="Token will be returned")

class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(allow_blank=True, required=False, help_text="Status will be returned")

class SubscriptionSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    address = serializers.CharField()
    city = serializers.CharField()
    state_code = serializers.CharField()
    postal_code = serializers.CharField()
    country_code = serializers.CharField()
    phone_country = serializers.CharField()
    phone_area = serializers.CharField()
    phone_number = serializers.CharField()
    addon_code = serializers.CharField()
    locator = serializers.CharField()
    cc_number = serializers.CharField(write_only=True)
    cc_exp = serializers.CharField(write_only=True)
    cc_cvv = serializers.CharField(write_only=True)
    subscribed_date = serializers.DateField()

    def create(self, validated_data):
        # Combine phone
        phone = f"+{validated_data['phone_country']}-{validated_data['phone_area']}-{validated_data['phone_number']}"

        # Create user
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # Mask CC info (store only last 4, NEVER store full number in production)
        cc_masked = f"**** **** **** {validated_data['cc_number'][-4:]}"
        exp_masked = f"**/**"
        cvv_masked = "***"

        # Save profile
        UserProfile.objects.create(
            user=user,
            address=validated_data['address'],
            city=validated_data['city'],
            state_code=validated_data['state_code'],
            country_code=validated_data['country_code'],
            postal_code=validated_data['postal_code'],
            phone=phone,
            subscribed_package=validated_data['addon_code'],
            subscribed_date=validated_data['subscribed_date']
        )

        # Save subscription history
        SubscriptionHistory.objects.create(
            user=user,
            subscribed_package=validated_data['addon_code'],
            subscribed_date=validated_data['subscribed_date']
        )

        # Save masked data to ApplicationToken (or another secure model if you prefer)
        ApplicationToken.objects.create(
            user=user,
            application='SUBSCRIPTION',
            token=cc_masked,
            custom1=exp_masked,
            custom2=cvv_masked,
            custom3=validated_data['locator']
        )

        return user