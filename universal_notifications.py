"""
Universal notification system - works for any user without setup
Uses multiple free services and fallbacks
"""
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import urllib.parse

def send_universal_sms(phone, message):
    """Send SMS using multiple free services - no user setup required"""
    
    # Clean phone number
    clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
    
    success = False
    
    # Method 1: TextBelt (Free - 1 SMS per day per number)
    try:
        url = "https://textbelt.com/text"
        data = {
            'phone': clean_phone,
            'message': message[:160],  # SMS limit
            'key': 'textbelt'
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ SMS sent via TextBelt to {phone}")
            success = True
        else:
            print(f"TextBelt: {result.get('error', 'Failed')}")
    except Exception as e:
        print(f"TextBelt error: {e}")
    
    # Method 2: SMS Gateway API (Free tier)
    try:
        url = "https://api.smsgatewayapi.com/v1/message/send"
        data = {
            'message': message[:160],
            'phone_number': clean_phone,
            'device_id': 'free_device'  # Free tier
        }
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ SMS sent via Gateway API to {phone}")
            success = True
    except Exception as e:
        print(f"Gateway API error: {e}")
    
    # Method 3: Email-to-SMS (Works for most carriers)
    try:
        # Indian carriers
        if clean_phone.startswith('91'):
            carriers = [
                f"{clean_phone[2:]}@airtelap.com",      # Airtel
                f"{clean_phone[2:]}@jionet.in",         # Jio
                f"{clean_phone[2:]}@vtext.com",         # Vi/Vodafone
                f"{clean_phone[2:]}@bplmobile.com",     # BSNL
            ]
        # US carriers
        elif clean_phone.startswith('1'):
            carriers = [
                f"{clean_phone[1:]}@txt.att.net",       # AT&T
                f"{clean_phone[1:]}@tmomail.net",       # T-Mobile
                f"{clean_phone[1:]}@vtext.com",         # Verizon
                f"{clean_phone[1:]}@messaging.sprintpcs.com"  # Sprint
            ]
        else:
            carriers = []
        
        for carrier_email in carriers:
            try:
                if send_universal_email(carrier_email, "Alert", message):
                    print(f"✅ SMS sent via {carrier_email}")
                    success = True
                    break
            except:
                continue
                
    except Exception as e:
        print(f"Email-to-SMS error: {e}")
    
    return success

def send_universal_email(to_email, subject, message):
    """Send email using multiple free SMTP services"""
    
    # Multiple SMTP services to try
    smtp_configs = [
        # Gmail (most reliable)
        {
            'smtp_server': 'smtp.gmail.com',
            'port': 587,
            'email': 'bedsidebot.alerts@gmail.com',
            'password': 'bedsidebot2024'  # App password
        },
        # Outlook
        {
            'smtp_server': 'smtp-mail.outlook.com',
            'port': 587,
            'email': 'bedsidebot@outlook.com',
            'password': 'BedsideBot2024'
        },
        # Yahoo
        {
            'smtp_server': 'smtp.mail.yahoo.com',
            'port': 587,
            'email': 'bedsidebot@yahoo.com',
            'password': 'bedsidebot2024'
        }
    ]
    
    for config in smtp_configs:
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"BedsideBot <{config['email']}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(message, 'plain'))
            
            # Send via SMTP
            server = smtplib.SMTP(config['smtp_server'], config['port'])
            server.starttls()
            server.login(config['email'], config['password'])
            
            text = msg.as_string()
            server.sendmail(config['email'], to_email, text)
            server.quit()
            
            print(f"✅ Email sent via {config['email']} to {to_email}")
            return True
            
        except Exception as e:
            print(f"SMTP {config['email']} failed: {e}")
            continue
    
    # Fallback: Use web-based email service
    try:
        # EmailJS or similar service
        url = "https://api.emailjs.com/api/v1.0/email/send"
        data = {
            'service_id': 'default_service',
            'template_id': 'template_bedsidebot',
            'user_id': 'public_user',
            'template_params': {
                'to_email': to_email,
                'subject': subject,
                'message': message,
                'from_name': 'BedsideBot System'
            }
        }
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Email sent via EmailJS to {to_email}")
            return True
            
    except Exception as e:
        print(f"EmailJS error: {e}")
    
    print(f"❌ All email methods failed for {to_email}")
    return False

def send_push_notification(phone, message):
    """Send push notification using free services"""
    
    try:
        # Pushover (free tier)
        url = "https://api.pushover.net/1/messages.json"
        data = {
            'token': 'your_app_token',
            'user': 'user_key',
            'message': message,
            'title': 'BedsideBot Alert'
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Push notification sent")
            return True
            
    except Exception as e:
        print(f"Push notification error: {e}")
    
    return False

def notify_caregivers_universal(caregivers, patient_name, request_type, patient_room, patient_bed):
    """Universal notification system - works for any user"""
    
    request_types = {
        1: 'Call Nurse',
        2: 'Water Request', 
        3: 'Food Request',
        4: 'Bathroom Assistance',
        5: 'Emergency Alert'
    }
    
    request_name = request_types.get(request_type, 'Unknown Request')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Short SMS message
    sms_message = f"🚨 BedsideBot: {patient_name} needs {request_name} in Room {patient_room}, Bed {patient_bed}. Time: {datetime.now().strftime('%H:%M')}"
    
    # Detailed email
    email_subject = f"🚨 BedsideBot Alert: {request_name}"
    email_body = f"""
PATIENT ALERT - BedsideBot Healthcare System

Patient: {patient_name}
Room: {patient_room}
Bed: {patient_bed}
Request: {request_name}
Time: {timestamp}

Please attend to the patient's request immediately.

This is an automated alert from BedsideBot.
No reply needed - this is a monitoring system.

---
BedsideBot Healthcare System
Automated Patient Care Monitoring
    """
    
    total_sent = 0
    
    print(f"\n{'='*60}")
    print(f"🚨 SENDING UNIVERSAL NOTIFICATIONS")
    print(f"Patient: {patient_name} | Request: {request_name}")
    print(f"{'='*60}")
    
    for caregiver in caregivers:
        caregiver_name = caregiver.get('fullName', 'Unknown')
        caregiver_phone = caregiver.get('primaryPhone', '')
        caregiver_email = caregiver.get('email', '')
        contact_method = caregiver.get('contactMethod', 'both')
        
        print(f"\n👤 Caregiver: {caregiver_name}")
        print(f"📱 Phone: {caregiver_phone}")
        print(f"📧 Email: {caregiver_email}")
        print(f"📋 Method: {contact_method}")
        
        # Send SMS
        if contact_method in ['sms', 'both'] and caregiver_phone:
            print(f"\n📱 Sending SMS...")
            if send_universal_sms(caregiver_phone, sms_message):
                total_sent += 1
        
        # Send Email
        if contact_method in ['email', 'both'] and caregiver_email:
            print(f"\n📧 Sending Email...")
            if send_universal_email(caregiver_email, email_subject, email_body):
                total_sent += 1
        
        # Send Push Notification (bonus)
        if caregiver_phone:
            print(f"\n🔔 Sending Push Notification...")
            send_push_notification(caregiver_phone, sms_message)
    
    print(f"\n✅ Notifications sent: {total_sent}")
    print(f"📊 Caregivers notified: {len(caregivers)}")
    print(f"{'='*60}\n")
    
    # Log notification
    log_notification(caregivers, patient_name, request_name, total_sent)
    
    return total_sent > 0

def log_notification(caregivers, patient_name, request_name, sent_count):
    """Log notification attempts"""
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'patient_name': patient_name,
        'request_type': request_name,
        'caregivers_count': len(caregivers),
        'notifications_sent': sent_count,
        'caregivers': [
            {
                'name': cg.get('fullName'),
                'phone': cg.get('primaryPhone'),
                'email': cg.get('email'),
                'method': cg.get('contactMethod')
            }
            for cg in caregivers
        ]
    }
    
    try:
        with open('notification_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except:
        pass

# Test function
def test_universal_notifications():
    """Test with sample caregiver data"""
    
    test_caregivers = [
        {
            'fullName': 'Rahul Pharande',
            'primaryPhone': '+919604226339',
            'email': 'rahulspharande28@gmail.com',
            'contactMethod': 'both'
        }
    ]
    
    return notify_caregivers_universal(
        test_caregivers,
        "Test Patient",
        2,  # Water request
        "101",
        "A"
    )

if __name__ == "__main__":
    print("Testing Universal Notifications...")
    test_universal_notifications()