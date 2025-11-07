# 📱 BedsideBot Notification Setup Guide

## Overview
The BedsideBot system now includes SMS and Email notifications that are sent to caregivers whenever patients make requests (water, food, nurse, bathroom, emergency).

## 🔧 Configuration Steps

### 1. Email Notifications Setup (Gmail)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings → Security
   - Enable 2-Step Verification
   - Go to App Passwords
   - Generate password for "Mail"
   - Copy the 16-character password

3. **Update .env file**:
   ```
   EMAIL_SENDER=rahulspharande28@gmail.com
   EMAIL_PASSWORD=your_16_character_app_password_here
   ```

### 2. SMS Notifications Setup (Twilio)

1. **Create Twilio Account**:
   - Sign up at https://www.twilio.com
   - Get free trial credits ($15)

2. **Get Credentials**:
   - Account SID (from Twilio Console)
   - Auth Token (from Twilio Console)
   - Phone Number (get a Twilio phone number)

3. **Update .env file**:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE=+1234567890
   ```

### 3. Alternative SMS Options (Free)

If you don't want to use Twilio, you can use these free alternatives:

#### Option A: Email-to-SMS Gateway
Many carriers support email-to-SMS. Update the notification code to send emails to:
- Airtel: `9604226339@airtelap.com`
- Jio: `9604226339@jionet.in`
- Vi/Vodafone: `9604226339@vtext.com`

#### Option B: WhatsApp Business API (Free Tier)
- Use WhatsApp Business API
- 1000 free messages per month

## 🚀 How It Works

### 1. Caregiver Registration
When you register a caregiver in the system:
```json
{
  "fullName": "Rahul Pharande",
  "primaryPhone": "+919604226339",
  "email": "rahulspharande28@gmail.com",
  "contactMethod": "both"  // "email", "sms", or "both"
}
```

### 2. Patient Request Flow
1. Patient makes request (gesture/voice)
2. System identifies request type
3. Finds all registered caregivers
4. Sends notifications based on caregiver preferences
5. Logs notification status

### 3. Notification Content
**SMS Example:**
```
🚨 BedsideBot Alert: John Doe in Room 101, Bed A needs: Water Request. Time: 14:30
```

**Email Example:**
```
Subject: 🚨 BedsideBot Alert: Water Request

PATIENT ALERT - BedsideBot System

Patient: John Doe
Room: 101
Bed: A
Request: Water Request
Time: 2024-01-15 14:30:25

Please attend to the patient's request immediately.

- BedsideBot Healthcare System
```

## 🧪 Testing the System

### 1. Quick Test
1. Start the application: `python app.py`
2. Go to: `http://localhost:5000/test_notifications`
3. Click "Send Test Notification"

### 2. Full Test Flow
1. Register Hospital: `http://localhost:5000/hospital`
2. Register Staff: `http://localhost:5000/staff`
3. Register Patient: `http://localhost:5000/patient`
4. Register Caregiver: `http://localhost:5000/caregiver`
   - Enter your phone: `+919604226339`
   - Enter your email: `rahulspharande28@gmail.com`
   - Set contact method: "both"
5. Go to Patient Interface: `http://localhost:5000/interface`
6. Simulate patient requests

### 3. API Testing
```bash
# Test notification endpoint
curl -X POST http://localhost:5000/test_notification

# Simulate patient request
curl -X POST http://localhost:5000/set_button \
  -H "Content-Type: application/json" \
  -d '{"button": 2}'

# Simulate voice command
curl -X POST http://localhost:5000/simulate_voice_request \
  -H "Content-Type: application/json" \
  -d '{"command": "water"}'
```

## 🔍 Troubleshooting

### Email Issues
- **"Authentication failed"**: Check app password, not regular password
- **"Less secure apps"**: Use app password instead
- **"SMTP error"**: Check internet connection

### SMS Issues
- **"Authentication failed"**: Verify Twilio credentials
- **"Invalid phone number"**: Use international format (+919604226339)
- **"Insufficient funds"**: Check Twilio account balance

### General Issues
- **"No caregivers registered"**: Register at least one caregiver first
- **"Notifications not sending"**: Check .env file configuration
- **"Import errors"**: Install requests library: `pip install requests`

## 📋 Current Configuration

**Default Caregiver (Fallback):**
- Name: Rahul Pharande
- Phone: +919604226339
- Email: rahulspharande28@gmail.com

**Supported Request Types:**
1. Call Nurse
2. Water Request
3. Food Request
4. Bathroom Assistance
5. Emergency Alert

## 🔒 Security Notes

- Never commit .env file to git
- Use app passwords for email
- Rotate Twilio tokens regularly
- Validate phone numbers before sending
- Rate limit notifications to prevent spam

## 📞 Support

If you need help setting up notifications:
1. Check the console logs for error messages
2. Test with the notification test page
3. Verify all credentials in .env file
4. Ensure internet connectivity

The system will work even if notifications fail - patient requests are still logged and displayed in the interface.