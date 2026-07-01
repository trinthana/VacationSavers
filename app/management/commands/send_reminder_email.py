import json
import requests

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from app.models import EmailUnsubscribe

import os
from django.conf import settings

User = get_user_model()

CAMPAIGNER_API_KEY = "8831bdf3-663b-4692-80ab-fb1729ddce57"
CAMPAIGNER_ENDPOINT = "https://edapi.campaigner.com/v1/RelaySends/"
PROFILE_GROUP_ID = "11293"

SITE_URL = "https://www.vacationsavers.com"


def should_send_reminder(user, offset_days):
    today = timezone.now().date()
    joined_date = user.date_joined.date()

    send_date = joined_date + timedelta(days=offset_days)

    while send_date <= today:
        if today == send_date:
            return True
        send_date = send_date + relativedelta(months=3)

    return False


def get_unsubscribe_link(user):
    unsubscribe, _ = EmailUnsubscribe.objects.get_or_create(user=user)
    return f"{SITE_URL}/unsubscribe/{unsubscribe.token}/"


def send_campaigner_email2(email, first_name, subject, html_content):
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

    headers = {
        "ApiKey": CAMPAIGNER_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            CAMPAIGNER_ENDPOINT + PROFILE_GROUP_ID,
            headers=headers,
            data=json.dumps(payload),
        )
        print(f"✅ Campaigner response for {email}: {response.status_code}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Campaigner error for {email}: {str(e)}")
        return False

def send_campaigner_email(email, first_name, subject, html_content):
    if getattr(settings, "EMAIL_TEST_MODE", False):
        output_dir = getattr(settings, "EMAIL_TEST_OUTPUT_DIR", "email_previews")
        os.makedirs(output_dir, exist_ok=True)

        safe_email = email.replace("@", "_at_").replace(".", "_")
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_email}.html"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ Email preview saved: {filepath}")
        return True

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

    headers = {
        "ApiKey": CAMPAIGNER_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            CAMPAIGNER_ENDPOINT + PROFILE_GROUP_ID,
            headers=headers,
            data=json.dumps(payload),
        )
        print(f"✅ Campaigner response for {email}: {response.status_code}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Campaigner error for {email}: {str(e)}")
        return False
    
def build_email_html(title, greeting, intro_html, cta_url, cta_text, benefits_html, unsubscribe_link):
    current_year = datetime.now().year

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title} - VacationSavers</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
            <div style="text-align: center;">
                <img src="https://www.vacationsavers.com/static/assets/images/logo.png"
                     alt="VacationSavers"
                     style="width: 300px;" />
            </div>

            <h2 style="color: #2a2a2a; text-align: center;">{title}</h2>

            <p>{greeting}</p>

            {intro_html}

            <p style="text-align: center; margin: 30px 0;">
                <a href="{cta_url}"
                   style="background-color:#f4c22b;color:white;padding:14px 30px;text-decoration:none;border-radius:6px;">
                    {cta_text}
                </a>
            </p>

            <div style="font-size: 16px; color: #333333; line-height: 1.6; margin-top: 20px;">
                {benefits_html}
            </div>

            <hr style="margin-top:30px;margin-bottom:20px;border:none;border-top:1px solid #ddd;">

            <p style="font-size:12px;color:#777;text-align:center;">
                If you no longer wish to receive these emails,
                <a href="{unsubscribe_link}">unsubscribe here</a>.
            </p>

            <p style="text-align: center; font-size: 12px; color: #777;">
                &copy; {current_year} VacationSavers. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """


def send_reminder_email(user):
    first_name = user.get_full_name() or user.username
    unsubscribe_link = get_unsubscribe_link(user)

    subject = "Reminder: Use Your VacationSavers Membership – Explore Now"

    html_content = build_email_html(
        title="Use Your VacationSavers Membership – Explore Now",
        greeting=f"Hi {first_name} ({user.username}),",
        intro_html="""
            <p>Don’t miss out on your VacationSavers exclusive benefits.</p>
            <p>Start exploring today and see how far your savings can take you!</p>
        """,
        cta_url=f"{SITE_URL}/accounts/login/",
        cta_text="Start Saving Now",
        benefits_html="""
            <p>VacationSavers members get:</p>
            <ul style="padding-left: 20px;">
                <li>5% off all flights (up to $20 per ticket)</li>
                <li>Save up to 60% on vacation rentals</li>
                <li>Exclusive deals on hotels, activities, cruises, and more</li>
            </ul>
            <p>Your savings are just one click away. Explore your travel perks today!</p>
        """,
        unsubscribe_link=unsubscribe_link,
    )

    return send_campaigner_email(user.email, first_name, subject, html_content)


def send_lodging_email(user):
    first_name = user.get_full_name() or user.username
    unsubscribe_link = get_unsubscribe_link(user)

    subject = "Don’t Miss Out on Member-Only Hotel and Rental Deals"

    html_content = build_email_html(
        title="Have you checked out your lodging perks yet?",
        greeting=f"Hi {first_name} ({user.username}),",
        intro_html="""
            <p>VacationSavers members save big on hotels, vacation rentals, and resorts around the world.
            Whether you're booking a weekend stay or a full vacation, your exclusive rates can help you save up to 60%.</p>
        """,
        cta_url=f"{SITE_URL}/vacation-rentals-gtn/",
        cta_text="See Lodging Deals",
        benefits_html="""
            <ul style="padding-left: 20px;">
                <li>Discounts up to $90 per night on hotel bookings</li>
                <li>Save up to 60% on vacation rentals</li>
                <li>Incredible deals at resorts throughout North America and the Caribbean</li>
            </ul>
        """,
        unsubscribe_link=unsubscribe_link,
    )

    return send_campaigner_email(user.email, first_name, subject, html_content)


def send_carrental_email(user):
    first_name = user.get_full_name() or user.username
    unsubscribe_link = get_unsubscribe_link(user)

    subject = "Save on Car Rentals with Your Membership"

    html_content = build_email_html(
        title="VacationSavers includes discounted car rental rates",
        greeting=f"Hi {first_name} ({user.username}),",
        intro_html="""
            <p>Members enjoy special rates on top car rental brands in cities and airports across the globe.
            Whether it’s for business, a road trip, or a beach getaway, we’ve got you covered.</p>
        """,
        cta_url=f"{SITE_URL}/car-access/",
        cta_text="View Car Rental Deals",
        benefits_html="""
            <ul style="padding-left: 20px;">
                <li>Save up to 25% on car rentals from brands you trust</li>
                <li>Pay Now or Later. Conveniently flexible - pay upfront or at pick up</li>
                <li>Free Cancellation - No charge to cancel up to 48 hours before pick up</li>
            </ul>
        """,
        unsubscribe_link=unsubscribe_link,
    )

    return send_campaigner_email(user.email, first_name, subject, html_content)


def send_activity_email(user):
    first_name = user.get_full_name() or user.username
    unsubscribe_link = get_unsubscribe_link(user)

    subject = "Theme Park Tickets, Tours & More – For Less"

    html_content = build_email_html(
        title="Ready for fun? Your membership unlocks savings on theme parks, attractions, and activities",
        greeting=f"Hi {first_name} ({user.username}),",
        intro_html="""
            <p>From rollercoasters and guided tours to zip lines and sunset cruises,
            members get exclusive deals on experiences you won’t want to miss.</p>
            <p>Log in today to explore your perks and save on your next adventure!</p>
        """,
        cta_url=f"{SITE_URL}/access-travel/",
        cta_text="Discover Activities & Attractions",
        benefits_html="""
            <ul style="padding-left: 20px;">
                <li>Access exclusive discounts on theme parks</li>
                <li>Save up to 70% on organized tours in top destinations worldwide, from Italy to Japan to Egypt</li>
                <li>Tickets for Sports, Concerts, or Theater</li>
            </ul>
        """,
        unsubscribe_link=unsubscribe_link,
    )

    return send_campaigner_email(user.email, first_name, subject, html_content)


def send_summary_email(date, content, email, to_name="Admin"):
    subject = "Summarized Reminder Email Sending finished at " + date
    return send_campaigner_email(email, to_name, subject, content)


class Command(BaseCommand):
    help = "Send reminder emails to users who never logged in."

    def handle(self, *args, **options):
        now = timezone.now()
        start_time = now.strftime("%Y-%m-%d %H:%M:%S")

        self.stdout.write(f"========== Start at {start_time} ==========")

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Reminder Email Summary</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
                <h2 style="color: #2a2a2a; text-align: center;">========== Start at {start_time} ==========</h2>
        """

        users = (
            User.objects
            .filter(last_login__isnull=True, is_active=True)
            .exclude(email="")
            .exclude(emailunsubscribe__is_unsubscribed=True)
        )

        reminder_users = []
        lodging_users = []
        carrental_users = []
        activities_users = []

        for user in users:
            if should_send_reminder(user, 4):
                reminder_users.append(user)

            if should_send_reminder(user, 8):
                lodging_users.append(user)

            if should_send_reminder(user, 12):
                carrental_users.append(user)

            if should_send_reminder(user, 16):
                activities_users.append(user)

        total_count = (
            len(reminder_users)
            + len(lodging_users)
            + len(carrental_users)
            + len(activities_users)
        )

        self.stdout.write(f"Found {total_count} users eligible for sending email.")

        email_groups = [
            ("Reminder Emails", reminder_users, send_reminder_email, "reminder"),
            ("Lodging Emails", lodging_users, send_lodging_email, "lodging"),
            ("Car Rentals Emails", carrental_users, send_carrental_email, "car rentals"),
            ("Activities Emails", activities_users, send_activity_email, "activities"),
        ]

        for group_title, group_users, sender_func, label in email_groups:
            html_content += f"""
                <h2 style="color: #2a2a2a; text-align: center;">========== {group_title} ==========</h2>
            """

            for user in group_users:
                success = sender_func(user)

                sent_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

                html_content += f"""
                    <p>{sent_time} ==> {user.email}</p>
                """

                if success:
                    self.stdout.write(f"✅ On {sent_time} Succeeded to send {label} email to {user.email}")
                else:
                    self.stderr.write(f"❌ On {sent_time} Failed to send {label} email to {user.email}")

        html_content += """
            </div>
        </body>
        </html>
        """

        end_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        success = send_summary_email(
            end_time,
            html_content,
            "dmartin@lbftravel.com",
            "Doug",
        )

        if success:
            self.stdout.write(f"✅ On {end_time} Succeeded to send summary email to Doug")
        else:
            self.stderr.write(f"❌ On {end_time} Failed to send summary email to Doug")

        success = send_summary_email(
            end_time,
            html_content,
            "trin@lbftravel.com",
            "Trin",
        )

        if success:
            self.stdout.write(f"✅ On {end_time} Succeeded to send summary email to Trin")
        else:
            self.stderr.write(f"❌ On {end_time} Failed to send summary email to Trin")