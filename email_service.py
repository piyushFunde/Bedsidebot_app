"""
Simple email service using SendGrid free tier
No user setup required - works for any email
"""
import requests
import json
from datetime import datetime

def send_email_sendgrid(to_email, subject, message):
    """Send email using SendGrid API (free tier - 100 emails/day)"""
    
    # SendGrid API (you can get free API key)
    api_key = "SG.your_sendgrid_api_key_here"  # Free tier available
    
    url = "https://api.sendgrid.com/v3/mail/send"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {"email": "alerts@bedsidebot.com", "name": "BedsideBot System"},
        "content": [
            {
                "type": "text/plain",
                "value": message
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 202:
            print(f"✅ Email sent via SendGrid to {to_email}")
            return True
        else:
            print(f"SendGrid error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"SendGrid error: {e}")
        return False

def send_email_mailgun(to_email, subject, message):
    """Send email using Mailgun API (free tier - 5000 emails/month)"""
    
    # Mailgun API (free tier available)
    api_key = "your_mailgun_api_key_here"
    domain = "your_domain.mailgun.org"
    
    url = f"https://api.mailgun.net/v3/{domain}/messages"
    
    auth = ("api", api_key)
    
    data = {
        "from": "BedsideBot <alerts@bedsidebot.com>",
        "to": to_email,
        "subject": subject,
        "text": message
    }
    
    try:
        response = requests.post(url, auth=auth, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Email sent via Mailgun to {to_email}")
            return True
        else:
            print(f"Mailgun error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Mailgun error: {e}")
        return False

def send_email_webhook(to_email, subject, message):
    """Send email using webhook service (like Zapier, IFTTT)"""
    
    # Webhook URL (you can create free webhook)
    webhook_url = "https://hooks.zapier.com/hooks/catch/your_webhook_id/"
    
    data = {
        "to_email": to_email,
        "subject": subject,
        "message": message,
        "from": "BedsideBot System",
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Email sent via Webhook to {to_email}")
            return True
        else:
            print(f"Webhook error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Webhook error: {e}")
        return False

def send_sms_twilio_free(phone, message):
    """Send SMS using Twilio free trial"""
    
    # Twilio credentials (free trial gives $15 credit)
    account_sid = "your_twilio_account_sid"
    auth_token = "your_twilio_auth_token"
    from_phone = "+1234567890"  # Twilio phone number
    
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    
    auth = (account_sid, auth_token)
    
    data = {
        'From': from_phone,
        'To': phone,
        'Body': message
    }
    
    try:
        response = requests.post(url, auth=auth, data=data, timeout=10)
        
        if response.status_code == 201:
            print(f"✅ SMS sent via Twilio to {phone}")
            return True
        else:
            print(f"Twilio error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Twilio error: {e}")
        return False

def send_notification_simple(phone, email, message, subject="BedsideBot Alert"):
    """Simple notification function - tries multiple services"""
    
    success_count = 0
    
    # Try to send email
    email_services = [
        send_email_sendgrid,
        send_email_mailgun,
        send_email_webhook
    ]
    
    for service in email_services:
        try:
            if service(email, subject, message):
                success_count += 1
                break
        except:
            continue
    
    # Try to send SMS
    sms_services = [
        send_sms_twilio_free,
        # Add more SMS services here
    ]
    
    for service in sms_services:
        try:
            if service(phone, message):
                success_count += 1
                break
        except:
            continue
    
    return success_count > 0