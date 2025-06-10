import requests
import json
from datetime import datetime

CAMPAIGNER_API_KEY = "8831bdf3-663b-4692-80ab-fb1729ddce57"
CAMPAIGNER_ENDPOINT = "https://edapi.campaigner.com/v1/RelaySends/"
WELCOME_GROUP_ID = "11290"
PROFILE_GROUP_ID = "11293"


def send_welcome_email(email, first_name, username, password, login_link):
    current_year = datetime.now().year

    subject = "Welcome to VacationSavers - Your Passport to Exclusive Travel Savings!"

    html_content = f"""
    <!DOCTYPE html>
    <html>

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimal-ui">
        <title>Welcome to VacationSavers</title>
    </head>

    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div
            style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
            <div style="text-align: center; font-size: 12px; color: #777777; margin-top: 40px;">
                <img alt="VacationSavers.com" style="width: 300px; text-align: left important;"
                    src="https://www.vacationsavers.com/static/assets/images/logo.png">
            </div>

            <h2 style="text-align: center; color: #2a2a2a;">Welcome to VacationSavers – Your Passport to Exclusive Travel
            Savings!</h2>

            <div class="font-size: 16px; color: #333333; line-height: 1.6; margin-top: 20px;">
                <p>Thank you for joining VacationSavers! As a member, you’ve just unlocked a world of unbeatable travel
                    deals:</p>
                <ul style="padding-left: 20px;">
                    <li>5% off all flights (up to $20 per ticket)</li>
                    <li>Save up to 60% on vacation rentals</li>
                    <li>Access exclusive discounts on theme parks</li>
                    <li>Private and unpublished airfares</li>
                    <li>Deep discounts on hotels, lodging, tours, cruises, and more</li>
                </ul>
            </div>

            <div class="font-size: 16px; color: #333333; line-height: 1.6; margin-top: 20px;">
                <p>To access your exclusive travel discounts, click the button below or use your username and password:</p>
                <div style="font-size: 16px; font-weight: bold; color: coral; background-color: rgb(58, 214, 238); border: dotted 2px; margin-top: 20px; width: 400px; ">
                    <ul style="padding-left: 20px; list-style: none;">
                        <li>Username : { username } </li>
                        <li>Password : { password } </li>
                    </ul>
                </div>

                <p>Your membership can pay for itself with just one booking. Start exploring today and see how far your
                    savings can take you!</p>
                <p style="text-align:center; margin-top: 40px;">
                    <a href=" { login_link } "
                        style="background-color:#f4c22b;color:white;padding:14px 30px;text-decoration:none;border-radius:6px;">Start
                        Saving Now</a>
                </p>

            </div>

            <div style="text-align: center; font-size: 12px; color: #777777; margin-top: 40px;">
                &copy; { current_year } VacationSavers. All rights reserved.
            </div>
        </div>
    </body>

    </html>
    """
    # Replace {{ current_year }} with actual year
    html_content = html_content.replace("{ current_year }", str(current_year))

    payload = {
        "Subject": subject,
        "FromEmail": "welcome@vacationsavers.com",  # must be verified in Campaigner
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
            CAMPAIGNER_ENDPOINT + WELCOME_GROUP_ID, headers=headers, data=json.dumps(payload)
        )
        print(f"Campaigner success: {response.json()}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Campaigner error: {e.response.status_code} - {e.response.text}")
        return f"Campaigner error: {e.response.status_code} - {e.response.text}"


def send_password_reset_email(email, first_name, reset_link):
    current_year = datetime.now().year

    subject = "Reset Your Password to Start Saving with VacationSavers"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Password Reset - VacationSavers</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px;">
            <div style="text-align: center;">
                <img src="https://www.vacationsavers.com/static/assets/images/logo.png" alt="VacationSavers" style="width: 300px;" />
            </div>

            <h2 style="color: #2a2a2a; text-align: center;">Reset Your Password</h2>

            <p>Hi {first_name},</p>
            <p>You requested a password reset for your VacationSavers account. Click the button below to reset it:</p>

            <p style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" style="background-color: #f4c22b; color: white; padding: 14px 30px; text-decoration: none; border-radius: 6px;">Reset Password</a>
            </p>

            <p>If you didn’t request this, you can safely ignore this email.</p>

            <p style="text-align: center; font-size: 12px; color: #777;">
                &copy; {current_year} VacationSavers. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Replace {{ current_year }} with actual year
    html_content = html_content.replace("{ current_year }", str(current_year))

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
            CAMPAIGNER_ENDPOINT + PROFILE_GROUP_ID, headers=headers, data=json.dumps(payload)
        )
        print(f"Campaigner success: {response.json()}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Campaigner error: {e.response.status_code} - {e.response.text}")
        return f"Campaigner error: {e.response.status_code} - {e.response.text}"
