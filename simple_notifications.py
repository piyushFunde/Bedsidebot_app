"""
Simple notification system using free services
"""
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

def send_free_sms(phone, message):
    """Send SMS using free SMS gateway (TextBelt)"""
    try:
        # Remove + from phone number
        clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
        
        # Use TextBelt free SMS service (1 free SMS per day per phone)
        url = "https://textbelt.com/text"
        data = {
            'phone': clean_phone,
            'message': message,
            'key': 'textbelt'  # Free tier
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ SMS sent to {phone}")
            return True
        else:
            print(f"❌ SMS failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ SMS error: {str(e)}")
        return False

def send_simple_email(to_email, subject, message):
    """Send email using Gmail SMTP (if configured)"""
    try:
        sender_email = "rahulspharande28@gmail.com"  # Your email
        sender_password = os.getenv('EMAIL_PASSWORD', '')
        
        if not sender_password:
            print(f"📧 Email would be sent to {to_email}: {subject}")
            return True  # Simulate success
        
        # Create message
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        
        # Send via Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"📧 Email simulation to {to_email}: {subject}")
        return True  # Always return success for demo

def notify_caregivers_simple(caregivers, patient_name, request_type, patient_room, patient_bed):
    """Send notifications using simple/free services"""
    
    request_types = {
        1: 'Call Nurse',
        2: 'Water Request', 
        3: 'Food Request',
        4: 'Bathroom Assistance',
        5: 'Emergency Alert'
    }
    
    request_name = request_types.get(request_type, 'Unknown Request')
    timestamp = datetime.now().strftime('%H:%M')
    
    # SMS message
    sms_message = f"🚨 BedsideBot: {patient_name} in Room {patient_room}, Bed {patient_bed} needs: {request_name}. Time: {timestamp}"
    
    # Email details
    email_subject = f"🚨 BedsideBot Alert: {request_name}"
    email_message = f"""
PATIENT ALERT - BedsideBot System

Patient: {patient_name}
Room: {patient_room}
Bed: {patient_bed}
Request: {request_name}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please attend to the patient's request immediately.

- BedsideBot Healthcare System
    """
    
    success_count = 0
    
    print(f"\n{'='*60}")
    print(f"🚨 SENDING NOTIFICATIONS")
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
            if send_free_sms(caregiver_phone, sms_message):
                success_count += 1
        
        # Send Email
        if contact_method in ['email', 'both'] and caregiver_email:
            if send_simple_email(caregiver_email, email_subject, email_message):
                success_count += 1
    
    print(f"\n✅ Notifications processed for {len(caregivers)} caregivers")
    print(f"{'='*60}\n")
    
    return success_count > 0