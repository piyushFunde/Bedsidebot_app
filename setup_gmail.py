"""
Gmail Setup Helper - Generate App Password
"""
import webbrowser
import time

def setup_gmail_app_password():
    """Guide user through Gmail App Password setup"""
    
    print("🔐 GMAIL APP PASSWORD SETUP")
    print("=" * 50)
    print()
    print("To send real email notifications, you need a Gmail App Password.")
    print("This is different from your regular Gmail password.")
    print()
    print("📋 Steps to get App Password:")
    print("1. Enable 2-Factor Authentication on your Gmail")
    print("2. Go to Google Account Settings")
    print("3. Navigate to Security > App Passwords")
    print("4. Generate password for 'Mail'")
    print("5. Copy the 16-character password")
    print()
    
    choice = input("🌐 Open Gmail security settings now? (y/n): ").lower()
    
    if choice == 'y':
        print("🌐 Opening Gmail security settings...")
        webbrowser.open("https://myaccount.google.com/security")
        time.sleep(2)
        
        print("🌐 Opening App Passwords page...")
        webbrowser.open("https://myaccount.google.com/apppasswords")
        
        print()
        print("📝 After generating the App Password:")
        print("1. Copy the 16-character password")
        print("2. Paste it in the script when prompted")
        print("3. The format looks like: 'abcd efgh ijkl mnop'")
        print()
        
        app_password = input("📋 Enter your Gmail App Password: ").strip()
        
        if len(app_password) >= 16:
            # Update the working_notifications.py file
            with open('working_notifications.py', 'r') as f:
                content = f.read()
            
            # Replace the placeholder
            content = content.replace(
                '"abcd efgh ijkl mnop",  # Replace with your actual app password',
                f'"{app_password}",  # Your Gmail App Password'
            )
            
            with open('working_notifications.py', 'w') as f:
                f.write(content)
            
            print("✅ Gmail App Password saved!")
            return True
        else:
            print("❌ Invalid App Password format. Should be 16 characters.")
            return False
    
    return False

def setup_fast2sms():
    """Guide user through Fast2SMS setup for Indian numbers"""
    
    print("\n📱 FAST2SMS SETUP (For Indian SMS)")
    print("=" * 50)
    print()
    print("Fast2SMS provides free SMS for Indian numbers.")
    print()
    print("📋 Steps to get Fast2SMS API:")
    print("1. Go to fast2sms.com")
    print("2. Sign up with your mobile number")
    print("3. Verify your number")
    print("4. Get free credits (₹10)")
    print("5. Copy your API key")
    print()
    
    choice = input("🌐 Open Fast2SMS website now? (y/n): ").lower()
    
    if choice == 'y':
        print("🌐 Opening Fast2SMS...")
        webbrowser.open("https://www.fast2sms.com/")
        
        print()
        print("📝 After getting your API key:")
        api_key = input("📋 Enter your Fast2SMS API Key: ").strip()
        
        if len(api_key) > 10:
            # Update the working_notifications.py file
            with open('working_notifications.py', 'r') as f:
                content = f.read()
            
            # Replace the placeholder
            content = content.replace(
                'api_key = "your_fast2sms_api_key_here"',
                f'api_key = "{api_key}"'
            )
            
            with open('working_notifications.py', 'w') as f:
                f.write(content)
            
            print("✅ Fast2SMS API key saved!")
            return True
        else:
            print("❌ Invalid API key format.")
            return False
    
    return False

if __name__ == "__main__":
    print("🚀 BedsideBot Notification Setup")
    print("=" * 50)
    print()
    print("This will help you set up real SMS and Email notifications.")
    print("Your phone: +919604226339")
    print("Your email: rahulspharande28@gmail.com")
    print()
    
    # Setup Gmail
    gmail_setup = setup_gmail_app_password()
    
    # Setup SMS
    sms_setup = setup_fast2sms()
    
    print("\n🎯 SETUP SUMMARY")
    print("=" * 30)
    print(f"📧 Gmail: {'✅ Ready' if gmail_setup else '❌ Not configured'}")
    print(f"📱 SMS: {'✅ Ready' if sms_setup else '❌ Not configured'}")
    print()
    
    if gmail_setup or sms_setup:
        print("✅ You can now receive real notifications!")
        print("🚀 Run: python app.py")
        print("🧪 Test at: http://localhost:5000/test_notifications")
    else:
        print("⚠️ No services configured. Notifications will be simulated.")
    
    input("\nPress Enter to continue...")