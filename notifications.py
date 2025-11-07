import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_notification(caregiver_email, patient_name, request_type, patient_room, patient_bed):
    """Send email notification to caregiver"""
    try:
        sender_email = os.getenv('EMAIL_SENDER')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            print("[WARNING] Email credentials not configured")
            return False
        
        # Request type mapping
        request_types = {
            1: 'Call Nurse',
            2: 'Water Request', 
            3: 'Food Request',
            4: 'Bathroom Assistance',
            5: 'Emergency Alert'
        }
        
        request_name = request_types.get(request_type, 'Unknown Request')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = caregiver_email
        msg['Subject'] = f"🚨 BedsideBot Alert: {request_name}"
        
        # Email body
        body = f"""
        PATIENT ALERT - BedsideBot System
        
        Patient: {patient_name}
        Room: {patient_room}
        Bed: {patient_bed}
        Request: {request_name}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Please attend to the patient's request immediately.
        
        - BedsideBot Healthcare System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, caregiver_email, text)
        server.quit()
        
        print(f"[SUCCESS] Email sent to {caregiver_email}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send email: {str(e)}")
        return False

def send_sms_notification(caregiver_phone, patient_name, request_type, patient_room, patient_bed):
    """Send SMS notification using Twilio"""
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone = os.getenv('TWILIO_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone]):
            print("[WARNING] Twilio credentials not configured")
            return False
        
        # Request type mapping
        request_types = {
            1: 'Call Nurse',
            2: 'Water Request', 
            3: 'Food Request',
            4: 'Bathroom Assistance',
            5: 'Emergency Alert'
        }
        
        request_name = request_types.get(request_type, 'Unknown Request')
        
        # SMS message
        message = f"🚨 BedsideBot Alert: {patient_name} in Room {patient_room}, Bed {patient_bed} needs: {request_name}. Time: {datetime.now().strftime('%H:%M')}"
        
        # Send SMS using Twilio API
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        data = {
            'From': twilio_phone,
            'To': caregiver_phone,
            'Body': message
        }
        
        response = requests.post(url, data=data, auth=(account_sid, auth_token))
        
        if response.status_code == 201:
            print(f"[SUCCESS] SMS sent to {caregiver_phone}")
            return True
        else:
            print(f"[ERROR] Failed to send SMS: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Failed to send SMS: {str(e)}")
        return False

def send_whatsapp_notification(caregiver_phone, patient_name, request_type, patient_room, patient_bed):
    """Send WhatsApp notification using Twilio (alternative)"""
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if not all([account_sid, auth_token]):
            print("[WARNING] WhatsApp credentials not configured")
            return False
        
        # Request type mapping
        request_types = {
            1: 'Call Nurse',
            2: 'Water Request', 
            3: 'Food Request',
            4: 'Bathroom Assistance',
            5: 'Emergency Alert'
        }
        
        request_name = request_types.get(request_type, 'Unknown Request')
        
        # WhatsApp message
        message = f"🏥 *BedsideBot Alert*\n\n👤 Patient: {patient_name}\n🏠 Room: {patient_room}\n🛏️ Bed: {patient_bed}\n📋 Request: *{request_name}*\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nPlease attend to the patient immediately."
        
        # Send WhatsApp using Twilio API
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        data = {
            'From': 'whatsapp:+14155238886',  # Twilio WhatsApp sandbox number
            'To': f'whatsapp:{caregiver_phone}',
            'Body': message
        }
        
        response = requests.post(url, data=data, auth=(account_sid, auth_token))
        
        if response.status_code == 201:
            print(f"[SUCCESS] WhatsApp sent to {caregiver_phone}")
            return True
        else:
            print(f"[ERROR] Failed to send WhatsApp: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Failed to send WhatsApp: {str(e)}")
        return False

def notify_caregivers(caregivers, patient_name, request_type, patient_room, patient_bed):
    """Send notifications to all registered caregivers"""
    success_count = 0
    
    for caregiver in caregivers:
        caregiver_name = caregiver.get('fullName', 'Unknown')
        caregiver_email = caregiver.get('email')
        caregiver_phone = caregiver.get('primaryPhone')
        contact_method = caregiver.get('contactMethod', 'both')
        
        print(f"[INFO] Notifying caregiver: {caregiver_name}")
        
        # Send email notification
        if contact_method in ['email', 'both'] and caregiver_email:
            if send_email_notification(caregiver_email, patient_name, request_type, patient_room, patient_bed):
                success_count += 1
        
        # Send SMS notification
        if contact_method in ['sms', 'both'] and caregiver_phone:
            if send_sms_notification(caregiver_phone, patient_name, request_type, patient_room, patient_bed):
                success_count += 1
    
    return success_count > 0