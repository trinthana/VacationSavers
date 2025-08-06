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

def send_lodging_email(email, first_name, username):
    current_year = datetime.now().year
    subject = "Don’t Miss Out on Member-Only Hotel and Rental Deals"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Don’t Miss Out on Member-Only Hotel and Rental Deals - VacationSavers</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
            <div style="text-align: center;">
                <img src="https://www.vacationsavers.com/static/assets/images/logo.png" alt="VacationSavers" style="width: 300px;" />
            </div>

            <h2 style="color: #2a2a2a; text-align: center;">Have you checked out your lodging perks yet?</h2>

             <p>VacationSavers members save big on hotels, vacation rentals, and resorts around the world. Whether you're booking a weekend stay or a full vacation, your exclusive rates can help you save up to 60%.</p>

            <p style="text-align: center; margin: 30px 0;">
                <a href="https://www.vacationsavers.com/vacation-rentals-gtn/"
                    style="background-color:#f4c22b;color:white;padding:14px 30px;text-decoration:none;border-radius:6px;">See Lodging Deals</a>
            </p>

            <div class="font-size: 16px; color: #333333; line-height: 1.6; margin-top: 20px;">
                <ul style="padding-left: 20px;">
                    <li>Discounts up to $90 per night on hotel bookings</li>
                    <li>Save up to 60% on vacation rentals</li>
                    <li>Incredible deals at resorts throughout North America and the Caribbean</li>
                </ul>
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

def send_carrental_email(email, first_name, username):
    current_year = datetime.now().year
    subject = "Save on Car Rentals with Your Membership"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Save on Car Rentals with Your Membership - VacationSavers</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
            <div style="text-align: center;">
                <img src="https://www.vacationsavers.com/static/assets/images/logo.png" alt="VacationSavers" style="width: 300px;" />
            </div>

            <h2 style="color: #2a2a2a; text-align: center;">VacationSavers includes discounted car rental rates—often enough to pay for your membership with just one trip!</h2>

             <p>Members enjoy special rates on top car rental brands in cities and airports across the globe. Whether it’s for business, a road trip, or a beach getaway, we’ve got you covered.</p>

            <p style="text-align: center; margin: 30px 0;">
                <a href="https://www.vacationsavers.com/car-access/"
                    style="background-color:#f4c22b;color:white;padding:14px 30px;text-decoration:none;border-radius:6px;">View Car Rental Deals</a>
            </p>

            <div class="font-size: 16px; color: #333333; line-height: 1.6; margin-top: 20px;">
                <ul style="padding-left: 20px;">
                    <li>Save up to 25% on car rentals from brands you trust</li>
                    <li>Pay Now or Later. Conveniently flexible - pay upfront or at pick up</li>
                    <li>Free Cancellation - No charge to cancel up to 48 hours before pick up</li>
                </ul>
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

def send_activity_email(email, first_name, username):
    current_year = datetime.now().year
    subject = "Theme Park Tickets, Tours & More – For Less"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Theme Park Tickets, Tours & More – For Less - VacationSavers</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
            <div style="text-align: center;">
                <img src="https://www.vacationsavers.com/static/assets/images/logo.png" alt="VacationSavers" style="width: 300px;" />
            </div>

            <h2 style="color: #2a2a2a; text-align: center;">Ready for fun? Your membership unlocks savings on theme parks, attractions, and activities</h2>

            <p>From rollercoasters and guided tours to zip lines and sunset cruises, members get exclusive deals on experiences you won’t want to miss.</p>
            <p>Log in today to explore your perks and save on your next adventure!</p>

            <p style="text-align: center; margin: 30px 0;">
                <a href="https://www.vacationsavers.com/access-travel/"
                    style="background-color:#f4c22b;color:white;padding:14px 30px;text-decoration:none;border-radius:6px;">Discover Activities & Attractions</a>
            </p>

            <div class="font-size: 16px; color: #333333; line-height: 1.6; margin-top: 20px;">
                <ul style="padding-left: 20px;">
                    <li>Access exclusive discounts on theme parks</li>
                    <li>Save up to 70% on organized tours in top destinations worldwide, from Italy to Japan to Egypt</li>
                    <li>Tickets for Sports, Concerts, or Theater</li>
                </ul>
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

def send_summary_email(date, content):
    current_year = datetime.now().year
    subject = "Summarrized Reminder Email Sending finished at " + date

    html_content = content

    payload = {
        "Subject": subject,
        "FromEmail": "welcome@vacationsavers.com",
        "FromName": "VacationSavers",
        "ToEmail": "dmartin@lbftravel.com; trin@lbftravel.com;",
        "ToName": "Doug",
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
        return True
    except requests.exceptions.RequestException as e:
        return False

class Command(BaseCommand):
    help = "Send reminder emails to users who never logged in every 4 days after joining."

    def handle(self, *args, **options):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Send reminder emails to users who never logged in every 4 days after joining.</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
        """

        now = timezone.now()
        start_time = now.strftime('%Y-%m-%d %H:%M:%S')
        self.stdout.write(f"========== Start at {start_time} ==========")

        html_content = html_content + f"""
            <h2 style="color: #2a2a2a; text-align: center;">========== Start at {start_time} ==========</h2>
        """
    
        users = User.objects.filter(last_login__isnull=True, is_active=True).exclude(email='')

        reminder_users = []
        lodging_users = []
        carrental_users = []
        activities_users = []
        
        for user in users:
            days_since_join = (now.date() - user.date_joined.date()).days
            if days_since_join >= 4 and days_since_join % 4 == 0:
                reminder_users.append(user)

            if days_since_join >= 8 and days_since_join % 8 == 0:
                lodging_users.append(user)

            if days_since_join >= 12 and days_since_join % 12 == 0:
                carrental_users.append(user)

            if days_since_join >= 16 and days_since_join % 16 == 0:
                activities_users.append(user)

        self.stdout.write(f"Found {len(reminder_users) + len(lodging_users) + len(carrental_users) + len(activities_users)} users eligible for sending email.")

        html_content = html_content + f"""
            <h2 style="color: #2a2a2a; text-align: center;">========== Reminder Emails ==========</h2>
        """
        for user in reminder_users:
            success = send_reminder_email(
                user.email,
                user.get_full_name() or user.username,
                user.username
            )
            now = timezone.now()
            start_time = now.strftime('%Y-%m-%d %H:%M:%S')

            html_content = html_content + f"""
                <p> {start_time} ==> {user.email}</p>
            """

            if success:
                self.stdout.write(f"✅ On {start_time} Succedd to send reminder  email to {user.email}")
            else:
                self.stderr.write(f"❌ On {start_time} Failed to send reminder email to {user.email}")

        html_content = html_content + f"""
            <h2 style="color: #2a2a2a; text-align: center;">========== Lodging Emails ==========</h2>
        """
        for user in lodging_users:
            success = send_lodging_email(
                user.email,
                user.get_full_name() or user.username,
                user.username
            )
            now = timezone.now()
            start_time = now.strftime('%Y-%m-%d %H:%M:%S')

            html_content = html_content + f"""
                <p> {start_time} ==> {user.email}</p>
            """

            if success:
                self.stdout.write(f"✅ On {start_time} Succedd to send lodging email to {user.email}")
            else:
                self.stderr.write(f"❌ On {start_time} Failed to send lodging email to {user.email}")

        html_content = html_content + f"""
            <h2 style="color: #2a2a2a; text-align: center;">========== Car Rentals Emails ==========</h2>
        """
        for user in carrental_users:
            success = send_carrental_email(
                user.email,
                user.get_full_name() or user.username,
                user.username
            )
            now = timezone.now()
            start_time = now.strftime('%Y-%m-%d %H:%M:%S')

            html_content = html_content + f"""
                <p> {start_time} ==> {user.email}</p>
            """

            if success:
                self.stdout.write(f"✅ On {start_time} Succedd to send car rentals email to {user.email}")
            else:
                self.stderr.write(f"❌ On {start_time} Failed to send car rentals email to {user.email}")                

        html_content = html_content + f"""
            <h2 style="color: #2a2a2a; text-align: center;">========== Activities Emails ==========</h2>
        """
        for user in activities_users:
            success = send_activity_email(
                user.email,
                user.get_full_name() or user.username,
                user.username
            )
            now = timezone.now()
            start_time = now.strftime('%Y-%m-%d %H:%M:%S')

            html_content = html_content + f"""
                <p> {start_time} ==> {user.email}</p>
            """

            if success:
                self.stdout.write(f"✅ On {start_time} Succedd to send activities email to {user.email}")
            else:
                self.stderr.write(f"❌ On {start_time} Failed to send activities email to {user.email}")                

        html_content = html_content + f"""
            </div>
        </body>
        </html>
        """
        now = timezone.now()
        start_time = now.strftime('%Y-%m-%d %H:%M:%S')
        success = send_summary_email(
            start_time,
            html_content
        )
        if success:
            self.stdout.write(f"✅ On {start_time} Succedd to send summary email to Doug")
        else:
            self.stderr.write(f"❌ On {start_time} Failed to send summary email to Doug")                
