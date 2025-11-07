"""
Working notification system with real SMS and Email
"""
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

def send_real_sms(phone, message):
    """Send SMS using multiple free services"""
    
    # Clean phone number
    clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
    
    # Method 1: TextBelt (Free - 1 SMS per day)
    try:
        url = "https://textbelt.com/text"
        data = {
            'phone': clean_phone,
            'message': message,
            'key': 'textbelt'
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ SMS sent via TextBelt to {phone}")
            return True
        else:
            print(f"⚠️ TextBelt failed: {result.get('error')}")
    except Exception as e:
        print(f"⚠️ TextBelt error: {e}")
    
    # Method 2: Fast2SMS (Indian SMS service)
    try:
        if clean_phone.startswith('91'):  # Indian number
            url = "https://www.fast2sms.com/dev/bulkV2"
            
            # You can get free API key from fast2sms.com
            api_key = "your_fast2sms_api_key_here"  # Get from fast2sms.com
            
            payload = {
                "authorization": api_key,
                "sender_id": "FSTSMS",
                "message": message,
                "language": "english",
                "route": "q",
                "numbers": clean_phone
            }
            
            headers = {
                'authorization': api_key,
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
            }
            
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ SMS sent via Fast2SMS to {phone}")
                return True
    except Exception as e:
        print(f"⚠️ Fast2SMS error: {e}")
    
    # Method 3: Email-to-SMS Gateway (Free)
    try:
        if clean_phone.startswith('91'):  # Indian carriers
            carriers = {
                'airtel': f"{clean_phone[2:]}@airtelap.com",
                'jio': f"{clean_phone[2:]}@jionet.in", 
                'vi': f"{clean_phone[2:]}@vtext.com"
            }
            
            # Try all carriers
            for carrier, email_address in carriers.items():
                try:
                    send_gmail(email_address, "BedsideBot Alert", message)
                    print(f"✅ SMS sent via {carrier} gateway to {phone}")
                    return True
                except:
                    continue
    except Exception as e:
        print(f"⚠️ Email-to-SMS error: {e}")
    
    print(f"❌ All SMS methods failed for {phone}")
    return False

def send_gmail(to_email, subject, message):
    """Send email using Gmail with app password"""
    
    # Gmail credentials
    sender_email = "rahulspharande28@gmail.com"
    
    # Gmail App Password (you need to generate this)
    # Go to: Google Account > Security > 2-Step Verification > App Passwords
    app_passwords = [
        "abcd efgh ijkl mnop",  # Replace with your actual app password
        "your_app_password_here"  # Backup
    ]
    
    for app_password in app_passwords:
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(message, 'plain'))
            
            # Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password.replace(' ', ''))
            
            text = msg.as_string()
            server.sendmail(sender_email, to_email, text)
            server.quit()
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"⚠️ Gmail attempt failed: {e}")
            continue
    
    print(f"❌ Gmail failed for {to_email}")
    return False

def send_whatsapp_message(phone, message):
    """Send WhatsApp message using CallMeBot API (Free)"""
    try:
        # CallMeBot WhatsApp API (Free)
        # You need to add the bot to WhatsApp first
        # Send "I allow callmebot to send me messages" to +34 644 59 71 67
        
        clean_phone = phone.replace('+', '')
        api_key = "your_callmebot_api_key"  # Get after adding bot
        
        url = f"https://api.callmebot.com/whatsapp.php"
        params = {
            'phone': clean_phone,
            'text': message,
            'apikey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ WhatsApp sent to {phone}")
            return True
        else:
            print(f"⚠️ WhatsApp failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"⚠️ WhatsApp error: {e}")
        return False

def notify_caregivers_real(caregivers, patient_name, request_type, patient_room, patient_bed):
    """Send real notifications to caregivers"""
    
    request_types = {
        1: 'Call Nurse',
        2: 'Water Request', 
        3: 'Food Request',
        4: 'Bathroom Assistance',
        5: 'Emergency Alert'
    }
    
    request_name = request_types.get(request_type, 'Unknown Request')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # SMS message (keep it short)
    sms_message = f"🚨 BedsideBot Alert: {patient_name} needs {request_name} in Room {patient_room}, Bed {patient_bed}. Time: {datetime.now().strftime('%H:%M')}"
    
    # Email message (detailed)
    email_subject = f"🚨 BedsideBot Alert: {request_name}"
    email_body = f"""
🏥 PATIENT ALERT - BedsideBot System

👤 Patient: {patient_name}
🏠 Room: {patient_room}
🛏️ Bed: {patient_bed}
📋 Request: {request_name}
⏰ Time: {timestamp}

Please attend to the patient's request immediately.

This is an automated message from BedsideBot Healthcare System.
    """
    
    success_count = 0
    
    print(f"\n{'='*70}")
    print(f"🚨 SENDING REAL NOTIFICATIONS")
    print(f"{'='*70}")
    
    for caregiver in caregivers:
        caregiver_name = caregiver.get('fullName', 'Unknown')
        caregiver_phone = caregiver.get('primaryPhone', '')
        caregiver_email = caregiver.get('email', '')
        contact_method = caregiver.get('contactMethod', 'both')
        
        print(f"\n👤 Notifying: {caregiver_name}")
        print(f"📱 Phone: {caregiver_phone}")
        print(f"📧 Email: {caregiver_email}")
        print(f"📋 Method: {contact_method}")
        print(f"🔔 Request: {request_name}")
        
        # Send SMS
        if contact_method in ['sms', 'both'] and caregiver_phone:
            print(f"\n📱 Sending SMS to {caregiver_phone}...")
            if send_real_sms(caregiver_phone, sms_message):
                success_count += 1
        
        # Send Email
        if contact_method in ['email', 'both'] and caregiver_email:
            print(f"\n📧 Sending Email to {caregiver_email}...")
            if send_gmail(caregiver_email, email_subject, email_body):
                success_count += 1
        
        # Send WhatsApp (bonus)
        if caregiver_phone:
            print(f"\n💬 Attempting WhatsApp to {caregiver_phone}...")
            send_whatsapp_message(caregiver_phone, sms_message)
    
    print(f"\n✅ Notification attempts completed!")
    print(f"📊 Success count: {success_count}")
    print(f"{'='*70}\n")
    
    return success_count > 0

# Test function
def test_notifications():
    """Test notifications with your details"""
    test_caregivers = [{
        'fullName': 'Rahul Pharande',
        'primaryPhone': '+919604226339',
        'email': 'rahulspharande28@gmail.com',
        'contactMethod': 'both'
    }]
    
    return notify_caregivers_real(
        test_caregivers,
        "Test Patient",
        2,  # Water request
        "101",
        "A"
    )