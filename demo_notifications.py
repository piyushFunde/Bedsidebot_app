"""
Demo notification system that works without external credentials
"""
import json
from datetime import datetime

def send_demo_notification(caregiver_phone, caregiver_email, patient_name, request_type, patient_room, patient_bed):
    """Send demo notification (console output)"""
    
    request_types = {
        1: 'Call Nurse',
        2: 'Water Request', 
        3: 'Food Request',
        4: 'Bathroom Assistance',
        5: 'Emergency Alert'
    }
    
    request_name = request_types.get(request_type, 'Unknown Request')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Console notification
    print(f"\n{'='*60}")
    print(f"🚨 BEDSIDEBOT NOTIFICATION ALERT")
    print(f"{'='*60}")
    print(f"📱 SMS to: {caregiver_phone}")
    print(f"📧 Email to: {caregiver_email}")
    print(f"👤 Patient: {patient_name}")
    print(f"🏠 Room: {patient_room} | 🛏️ Bed: {patient_bed}")
    print(f"📋 Request: {request_name}")
    print(f"⏰ Time: {timestamp}")
    print(f"{'='*60}\n")
    
    # Save to log file
    log_entry = {
        'timestamp': timestamp,
        'caregiver_phone': caregiver_phone,
        'caregiver_email': caregiver_email,
        'patient_name': patient_name,
        'room': patient_room,
        'bed': patient_bed,
        'request_type': request_name,
        'status': 'demo_sent'
    }
    
    try:
        with open('notification_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except:
        pass
    
    return True

def notify_caregivers_demo(caregivers, patient_name, request_type, patient_room, patient_bed):
    """Demo version of caregiver notifications"""
    
    if not caregivers:
        # Use default caregiver
        caregivers = [{
            'fullName': 'Rahul Pharande',
            'primaryPhone': '+919604226339',
            'email': 'rahulspharande28@gmail.com',
            'contactMethod': 'both'
        }]
    
    success_count = 0
    
    for caregiver in caregivers:
        caregiver_name = caregiver.get('fullName', 'Unknown')
        caregiver_phone = caregiver.get('primaryPhone', '+919604226339')
        caregiver_email = caregiver.get('email', 'rahulspharande28@gmail.com')
        
        print(f"[INFO] Notifying caregiver: {caregiver_name}")
        
        if send_demo_notification(caregiver_phone, caregiver_email, patient_name, request_type, patient_room, patient_bed):
            success_count += 1
    
    return success_count > 0