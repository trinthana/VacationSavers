import json
import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

CAMPAIGNER_API_KEY = "8831bdf3-663b-4692-80ab-fb1729ddce57"
CAMPAIGNER_ENDPOINT = "https://edapi.campaigner.com/v1/RelaySends/"
PROFILE_GROUP_ID = "11293"

def send_reminder_email(email, first_name, username):
    current_year = datetime.now().year
    subject = "Reminder: Use Your VacationSavers Trial – Explore Now"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Use Your VacationSavers Trial – Explore Now - VacationSavers</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
            <div style="text-align: center;">
                <img src="https://www.vacationsavers.com/static/assets/images/logo.png" alt="VacationSavers" style="width: 300px;" />
            </div>

            <h2 style="color: #2a2a2a; text-align: center;">Use Your VacationSavers Trial – Explore Now </h2>

            <p>Hi {first_name} ( {username} ),</p>
            <p>Don’t miss out on your 30-day free trial of VacationSavers.</p>

            <p>Your membership can pay for itself with just one booking. Start exploring today and see how far your
                savings can take you!</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="https://www.vacationsavers.com/accounts/login/"
                    style="background-color:#f4c22b;color:white;padding:14px 30px;text-decoration:none;border-radius:6px;">Start
                    Saving Now</a>
            </p>

            <div class="font-size: 16px; color: #333333; line-height: 1.6; margin-top: 20px;">
                <p>With your free trial, you get:</p>
                <ul style="padding-left: 20px;">
                    <li>5% off all flights (up to $20 per ticket)</li>
                    <li>Save up to 60% on vacation rentals</li>
                    <li>Exclusive deals on hotels, activities, cruises, and more</li>
                </ul>
                <p>Your savings are just one click away. Explore your travel perks today!</p>  
            </div>

            <p style="text-align: center; font-size: 12px; color: #777;">
                &copy; {current_year} VacationSavers. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """

    payload = {
        "Subject": subject,
        "FromEmail": "welcome@vacationsavers.com",
        "FromName": "VacationSavers",
        "ToEmail": email,
        "ToName": first_name,
        "ReplyEmail": "support@vacationsavers.com",
        "HTML": html_content,
        "IsHtml": True,
    }

    headers = {"ApiKey": CAMPAIGNER_API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(
            CAMPAIGNER_ENDPOINT + PROFILE_GROUP_ID,
            headers=headers,
            data=json.dumps(payload)
        )
        print(f"✅ Campaigner response for {email}: {response.status_code}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Campaigner error for {email}: {str(e)}")
        return False

class Command(BaseCommand):
    help = "Send reminder emails to users who never logged in every 3 days after joining."

    def handle(self, *args, **options):
        now = timezone.now()
        users = User.objects.filter(last_login__isnull=True, is_active=True).exclude(email='')

        final_users = []
        for user in users:
            days_since_join = (now.date() - user.date_joined.date()).days
            if days_since_join >= 3 and days_since_join % 3 == 0:
                final_users.append(user)

        self.stdout.write(f"Found {len(final_users)} users eligible for reminder email.")

        for user in final_users:
            success = send_reminder_email(
                user.email,
                user.get_full_name() or user.username,
                user.username
            )
            if success:
                self.stdout.write(f"✅ Email sent to {user.email}")
            else:
                self.stderr.write(f"❌ Failed to send email to {user.email}")