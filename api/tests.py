# api/tests.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from app.models import UserProfile, SubscriptionHistory, ApplicationToken
import datetime

class SubscribeViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('Subscribe')
        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "address": "123 Test Ave",
            "city": "Testville",
            "state_code": "CA",
            "postal_code": "90210",
            "country_code": "US",
            "phone_country": "1",
            "phone_area": "310",
            "phone_number": "5551234",
            "addon_code": "PREMIER",
            "locator": "ABC123",
            "cc_number": "4111111111111111",
            "cc_exp": "12/25",
            "cc_cvv": "123",
            "subscribed_date": datetime.date.today().isoformat()
        }

    def test_subscribe_success(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_id', response.data)

        user = User.objects.get(username=self.valid_payload['email'])
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertTrue(SubscriptionHistory.objects.filter(user=user).exists())
        self.assertTrue(ApplicationToken.objects.filter(user=user, application="SUBSCRIPTION").exists())

    def test_subscribe_duplicate_email(self):
        # First subscription should succeed
        self.client.post(self.url, self.valid_payload, format='json')

        # Second with same email should fail
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_subscribe_missing_required_field(self):
        incomplete_payload = self.valid_payload.copy()
        del incomplete_payload['email']  # Required field

        response = self.client.post(self.url, incomplete_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_masked_card_data_storage(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        user = User.objects.get(username=self.valid_payload['email'])
        token_obj = ApplicationToken.objects.get(user=user, application="SUBSCRIPTION")
        
        self.assertTrue(token_obj.token.endswith("1111"))
        self.assertEqual(token_obj.custom1, "**/**")
        self.assertEqual(token_obj.custom2, "***")
        self.assertEqual(token_obj.custom3, self.valid_payload["locator"])