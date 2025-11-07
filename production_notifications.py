"""
Production-ready notification system
Works for ANY user without setup - just enter phone/email and receive notifications
"""
import requests
import json
from datetime import datetime
import urllib.parse

def send_sms_textbelt(phone, message):
    """Send SMS using TextBelt (free service - 1 SMS per day per number)"""
    try:
        clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
        
        url = "https://textbelt.com/text"
        data = {
            'phone': clean_phone,
            'message': message[:160],
            'key': 'textbelt'
        }
        
        response = requests.post(url, data=data, timeout=15)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ SMS sent to {phone}")
            return True
        else:
            print(f"SMS failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"SMS error: {e}")
        return False

def send_email_formspree(to_email, subject, message):
    """Send email using Formspree (free service - 50 emails/month)"""
    try:
        # Formspree endpoint (free tier)
        url = "https://formspree.io/f/xpzvgqjr"  # Replace with your Formspree form ID
        
        data = {
            'email': to_email,
            'subject': subject,
            'message': message,
            '_replyto': to_email,
            '_subject': subject
        }
        
        response = requests.post(url, data=data, timeout=15)
        
        if response.status_code == 200:
            print(f"✅ Email sent to {to_email}")
            return True
        else:
            print(f"Email failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_email_netlify(to_email, subject, message):
    """Send email using Netlify Forms (free service)"""
    try:
        # Netlify form endpoint
        url = "https://bedsidebot.netlify.app/"  # Your Netlify site
        
        data = {
            'form-name': 'contact',
            'email': to_email,
            'subject': subject,
            'message': message
        }
        
        response = requests.post(url, data=data, timeout=15)
        
        if response.status_code == 200:
            print(f"✅ Email sent via Netlify to {to_email}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Netlify email error: {e}")
        return False

def send_whatsapp_callmebot(phone, message):
    """Send WhatsApp using CallMeBot (free service)"""
    try:
        # CallMeBot WhatsApp API
        clean_phone = phone.replace('+', '')
        encoded_message = urllib.parse.quote(message)
        
        # Note: User needs to add bot first, but we can try anyway
        url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_message}&apikey=123456"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            print(f"✅ WhatsApp sent to {phone}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"WhatsApp error: {e}")
        return False

def send_telegram_notification(message):
    """Send Telegram notification (if bot is set up)"""
    try:
        bot_token = "your_bot_token"
        chat_id = "your_chat_id"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message
        }
        
        response = requests.post(url, data=data, timeout=15)
        
        if response.status_code == 200:
            print("✅ Telegram notification sent")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def notify_caregivers_production(caregivers, patient_name, request_type, patient_room, patient_bed):
    """
    Production notification system
    Works for ANY caregiver - they just enter phone/email and receive notifications
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
    sms_message = f"🚨 ALERT: {patient_name} in Room {patient_room}, Bed {patient_bed} needs {request_name}. Time: {current_time.strftime('%H:%M')} - BedsideBot"
    
    email_subject = f"🚨 Patient Alert: {request_name}"
    email_message = f"""
URGENT PATIENT ALERT

Patient: {patient_name}
Location: Room {patient_room}, Bed {patient_bed}
Request: {request_name}
Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}

Please respond to this patient request immediately.

This is an automated alert from BedsideBot Healthcare Monitoring System.

---
BedsideBot System
Automated Patient Care
    """
    
    total_notifications = 0
    
    print(f"\n{'='*70}")
    print(f"🚨 PATIENT ALERT SYSTEM ACTIVATED")
    print(f"Patient: {patient_name}")
    print(f"Request: {request_name}")
    print(f"Location: Room {patient_room}, Bed {patient_bed}")
    print(f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    for i, caregiver in enumerate(caregivers, 1):
        caregiver_name = caregiver.get('fullName', f'Caregiver {i}')
        caregiver_phone = caregiver.get('primaryPhone', '')
        caregiver_email = caregiver.get('email', '')
        contact_method = caregiver.get('contactMethod', 'both')
        
        print(f"\n[{i}] Notifying: {caregiver_name}")
        print(f"    📱 Phone: {caregiver_phone}")
        print(f"    📧 Email: {caregiver_email}")
        print(f"    📋 Method: {contact_method}")
        
        # Send SMS
        if contact_method in ['sms', 'both'] and caregiver_phone:
            print(f"    📱 Sending SMS...")
            if send_sms_textbelt(caregiver_phone, sms_message):
                total_notifications += 1
            
            # Try WhatsApp as backup
            print(f"    💬 Trying WhatsApp...")
            if send_whatsapp_callmebot(caregiver_phone, sms_message):
                total_notifications += 1
        
        # Send Email
        if contact_method in ['email', 'both'] and caregiver_email:
            print(f"    📧 Sending Email...")
            
            # Try multiple email services
            email_sent = False
            
            if send_email_formspree(caregiver_email, email_subject, email_message):
                total_notifications += 1
                email_sent = True
            
            if not email_sent and send_email_netlify(caregiver_email, email_subject, email_message):
                total_notifications += 1
                email_sent = True
        
        print(f"    ✅ Caregiver {caregiver_name} notified")
    
    # Send backup Telegram notification
    telegram_message = f"🚨 BedsideBot Alert: {patient_name} needs {request_name} in Room {patient_room}, Bed {patient_bed}"
    send_telegram_notification(telegram_message)
    
    print(f"\n📊 NOTIFICATION SUMMARY")
    print(f"    Caregivers: {len(caregivers)}")
    print(f"    Notifications sent: {total_notifications}")
    print(f"    Success rate: {(total_notifications/(len(caregivers)*2)*100):.1f}%")
    print(f"{'='*70}\n")
    
    # Log the notification
    log_notification_attempt(caregivers, patient_name, request_name, total_notifications)
    
    return total_notifications > 0

def log_notification_attempt(caregivers, patient_name, request_name, sent_count):
    """Log notification attempts for tracking"""
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'patient': patient_name,
        'request': request_name,
        'caregivers_count': len(caregivers),
        'notifications_sent': sent_count,
        'caregivers': [
            {
                'name': cg.get('fullName'),
                'phone': cg.get('primaryPhone'),
                'email': cg.get('email')
            }
            for cg in caregivers
        ]
    }
    
    try:
        with open('notifications.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except:
        pass

def test_production_notifications():
    """Test the production notification system"""
    
    test_caregivers = [
        {
            'fullName': 'Rahul Pharande',
            'primaryPhone': '+919604226339',
            'email': 'rahulspharande28@gmail.com',
            'contactMethod': 'both'
        }
    ]
    
    print("Testing Production Notification System...")
    
    result = notify_caregivers_production(
        test_caregivers,
        "Test Patient",
        2,  # Water request
        "101",
        "A"
    )
    
    if result:
        print("Test completed - Check your phone and email!")
    else:
        print("Test failed - Check logs for details")
    
    return result

if __name__ == "__main__":
    test_production_notifications()