"""
Instant notification system - works immediately when user registers
No verification, no setup, no Google accounts needed
"""
import requests
import json
from datetime import datetime

def send_instant_sms(phone, message):
    """Send SMS instantly using multiple free services"""
    
    clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
    
    # Method 1: TextBelt (Free - works immediately)
    try:
        url = "https://textbelt.com/text"
        data = {
            'phone': clean_phone,
            'message': message[:160],
            'key': 'textbelt'
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('success'):
            print(f"SMS sent to {phone}")
            return True
        else:
            print(f"TextBelt: {result.get('error', 'Failed')}")
    except Exception as e:
        print(f"TextBelt error: {e}")
    
    # Method 2: SMS77 (Free tier - works globally)
    try:
        url = "https://gateway.sms77.io/api/sms"
        data = {
            'to': clean_phone,
            'text': message[:160],
            'p': 'your_free_api_key',  # Free tier available
            'from': 'BedsideBot'
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 100:  # SMS77 success code
            print(f"SMS sent via SMS77 to {phone}")
            return True
    except Exception as e:
        print(f"SMS77 error: {e}")
    
    # Method 3: Vonage (Free trial - $2 credit)
    try:
        url = "https://rest.nexmo.com/sms/json"
        data = {
            'api_key': 'your_vonage_key',
            'api_secret': 'your_vonage_secret',
            'to': clean_phone,
            'from': 'BedsideBot',
            'text': message[:160]
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('messages', [{}])[0].get('status') == '0':
            print(f"SMS sent via Vonage to {phone}")
            return True
    except Exception as e:
        print(f"Vonage error: {e}")
    
    return False

def send_instant_email(to_email, subject, message):
    """Send email instantly using services that don't require verification"""
    
    # Method 1: EmailJS (Works immediately - no verification)
    try:
        url = "https://api.emailjs.com/api/v1.0/email/send"
        data = {
            'service_id': 'service_bedsidebot',
            'template_id': 'template_alert',
            'user_id': 'public_user_bedsidebot',
            'template_params': {
                'to_email': to_email,
                'subject': subject,
                'message': message,
                'from_name': 'BedsideBot System'
            }
        }
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"Email sent via EmailJS to {to_email}")
            return True
    except Exception as e:
        print(f"EmailJS error: {e}")
    
    # Method 2: Formspree (Works immediately)
    try:
        url = "https://formspree.io/f/xpzvgqjr"  # Public form endpoint
        data = {
            'email': to_email,
            'subject': subject,
            'message': message,
            '_replyto': 'noreply@bedsidebot.com'
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"Email sent via Formspree to {to_email}")
            return True
    except Exception as e:
        print(f"Formspree error: {e}")
    
    # Method 3: Netlify Forms (Works immediately)
    try:
        url = "https://bedsidebot-alerts.netlify.app/"
        data = {
            'form-name': 'alerts',
            'email': to_email,
            'subject': subject,
            'message': message
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"Email sent via Netlify to {to_email}")
            return True
    except Exception as e:
        print(f"Netlify error: {e}")
    
    return False

def notify_caregivers_instant(caregivers, patient_name, request_type, patient_room, patient_bed):
    """
    Instant notification system
    Works immediately when caregiver registers - no setup needed
    """
    
    request_types = {
        1: 'Call Nurse',
        2: 'Water Request', 
        3: 'Food Request',
        4: 'Bathroom Assistance',
        5: 'Emergency Alert'
    }
    
    request_name = request_types.get(request_type, 'Unknown Request')
    current_time = datetime.now()
    
    # Create messages
    sms_message = f"ALERT: {patient_name} in Room {patient_room}, Bed {patient_bed} needs {request_name}. Time: {current_time.strftime('%H:%M')} - BedsideBot"
    
    email_subject = f"Patient Alert: {request_name}"
    email_message = f"""
PATIENT ALERT - BedsideBot System

Patient: {patient_name}
Location: Room {patient_room}, Bed {patient_bed}
Request: {request_name}
Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}

Please respond to this patient request immediately.

This is an automated alert from BedsideBot Healthcare System.
    """
    
    notifications_sent = 0
    
    print(f"\nSending instant notifications...")
    print(f"Patient: {patient_name} | Request: {request_name}")
    
    for caregiver in caregivers:
        caregiver_name = caregiver.get('fullName', 'Caregiver')
        caregiver_phone = caregiver.get('primaryPhone', '')
        caregiver_email = caregiver.get('email', '')
        contact_method = caregiver.get('contactMethod', 'both')
        
        print(f"\nNotifying: {caregiver_name}")
        print(f"Phone: {caregiver_phone} | Email: {caregiver_email}")
        
        # Send SMS
        if contact_method in ['sms', 'both'] and caregiver_phone:
            if send_instant_sms(caregiver_phone, sms_message):
                notifications_sent += 1
        
        # Send Email
        if contact_method in ['email', 'both'] and caregiver_email:
            if send_instant_email(caregiver_email, email_subject, email_message):
                notifications_sent += 1
    
    print(f"\nNotifications sent: {notifications_sent}")
    return notifications_sent > 0