# -*- coding: utf-8 -*-
"""
Quick Setup for BedsideBot Notifications
"""
import webbrowser

def main():
    print("BedsideBot Notification Setup")
    print("=" * 40)
    print()
    print("To send real notifications to your phone (+919604226339)")
    print("and email (rahulspharande28@gmail.com), we need to set up:")
    print()
    print("1. Gmail App Password (for email notifications)")
    print("2. SMS service (for text messages)")
    print()
    
    # Gmail Setup
    print("STEP 1: Gmail App Password")
    print("-" * 30)
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Sign in to rahulspharande28@gmail.com")
    print("3. Enable 2-Factor Authentication if not enabled")
    print("4. Generate App Password for 'Mail'")
    print("5. Copy the 16-character password")
    print()
    
    choice = input("Open Gmail App Passwords page? (y/n): ")
    if choice.lower() == 'y':
        webbrowser.open("https://myaccount.google.com/apppasswords")
    
    print()
    app_password = input("Enter your Gmail App Password (16 chars): ").strip()
    
    if len(app_password) >= 16:
        # Update the notification file
        try:
            with open('working_notifications.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace(
                '"abcd efgh ijkl mnop"',
                f'"{app_password}"'
            )
            
            with open('working_notifications.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("Gmail App Password saved!")
        except Exception as e:
            print(f"Error saving: {e}")
    
    print()
    print("STEP 2: SMS Setup")
    print("-" * 20)
    print("For SMS, we'll use free services:")
    print("- TextBelt (1 free SMS per day)")
    print("- Email-to-SMS gateways")
    print()
    print("Setup complete! Now run: python app.py")
    print("Test at: http://localhost:5000/test_notifications")

if __name__ == "__main__":
    main()