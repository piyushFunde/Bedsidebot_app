# BedsideBot - Multi-Assistant Healthcare System

BedsideBot is an advanced patient care system that uses multiple recognition technologies including hand sign detection, voice recognition, emotion detection, and eye gaze tracking to help bedridden and physically disabled patients communicate their needs effectively.

## Features

### Recognition Systems
- **Hand Sign Detection**: Use finger gestures (1-5 fingers) to select patient needs
- **Voice Recognition**: Natural speech processing for voice commands
- **Emotion Detection**: Facial emotion analysis for patient monitoring
- **Eye Gaze Tracking**: Eye movement tracking for interface control(in progress)

### Patient Communication Options
1. **Call Nurse** - Request nursing assistance
2. **Water** - Request water or hydration
3. **Food** - Request food or meals
4. **Bathroom** - Request bathroom assistance
5. **Emergency** - Emergency alert system
  
### Multi-Page Registration System
- **Landing Page**: Introduction and system overview
- **Hospital Registration**: Register healthcare facility
- **Staff Registration**: Register medical staff and nurses
- **Patient Registration**: Register patients with communication preferences
- **Caregiver Registration**: Register family members and caregivers
- **Module Selection**: Choose active recognition modules
- **Patient Interface**: Real-time monitoring and communication

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera for video processing
- Microphone for voice recognition (optional)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   cd BedsideBot_Integrated
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Configure your email and SMS settings in `.env`:
   ```
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   CAREGIVER_EMAIL=caregiver@hospital.com
   
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE=+1234567890
   CAREGIVER_PHONE=+0987654321
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the System**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Start with the landing page and follow the registration process

## Usage Flow

### 1. Registration Process
1. **Landing Page** (`/`) - System overview and introduction
2. **Hospital Registration** (`/hospital`) - Register your healthcare facility
3. **Staff Registration** (`/staff`) - Add medical staff and nurses
4. **Patient Registration** (`/patient`) - Register patients with their communication needs
5. **Caregiver Registration** (`/caregiver`) - Add family members and caregivers
6. **Module Selection** (`/modules`) - Choose which recognition systems to activate

### 2. Patient Monitoring
1. **Patient Interface** (`/interface`) - Real-time monitoring system
2. Enter patient name and bed number
3. Select active recognition features
4. Start monitoring with live video feed
5. Monitor patient requests and actions
6. Receive real-time notifications

### 3. Recognition Systems
- **Hand Gestures**: Hold up 1-5 fingers to select options
- **Voice Commands**: Say "water", "food", "nurse", "bathroom", or "emergency"
- **Emotion Detection**: Automatic detection of patient emotions
- **Eye Gaze**: Look left, right, or center to select options

### Use Case Diagram:
<img width="1699" height="786" alt="Screenshot 2025-11-10 181952" src="https://github.com/user-attachments/assets/c4373a6d-5dda-4ec1-a4fb-8940e2c80d61" />


## API Endpoints

### Registration APIs
- `POST /api/register/hospital` - Register hospital
- `POST /api/register/staff` - Register staff member
- `POST /api/register/patient` - Register patient
- `POST /api/register/caregiver` - Register caregiver

### Monitoring APIs
- `GET /video_feed` - Live video stream
- `POST /start_monitoring` - Start patient monitoring
- `GET /get_selected_button` - Get current patient selection
- `POST /set_button` - Set patient selection
- `POST /listen_voice` - Voice recognition endpoint
- `POST /stop_monitoring` - Stop monitoring

## System Console

The patient interface includes a real-time console panel that displays:
- System initialization status
- Module loading information
- Patient registration events
- Recognition system activities
- Error messages and warnings
- Monitoring status updates

## Notification System

BedsideBot supports multiple notification methods:
- **Email Notifications**: Sent to configured caregiver email
- **SMS Notifications**: Sent via Twilio to caregiver phone
- **Real-time Interface**: Live updates on the monitoring screen

## Troubleshooting

### Common Issues

1. **Camera Not Working**
   - Ensure webcam is connected and not used by other applications
   - Check camera permissions in your operating system

2. **Voice Recognition Not Working**
   - Ensure microphone is connected and working
   - Check microphone permissions
   - Verify SpeechRecognition library is properly installed

3. **Email/SMS Not Sending**
   - Verify email and Twilio credentials in `.env` file
   - Check internet connection
   - Ensure email app passwords are configured correctly

4. **Module Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Try reinstalling specific packages that are failing

### Performance Optimization

- For better performance, ensure good lighting for camera-based recognition
- Use a high-quality webcam for better hand gesture and emotion detection
- Ensure stable internet connection for notifications
- Close unnecessary applications to free up system resources

## Security Considerations

- All patient data is stored locally during the session
- Use HTTPS in production environments
- Secure your `.env` file and never commit it to version control
- Regularly update dependencies for security patches

## Support

For technical support or questions:
- Check the console panel for real-time system status
- Review error messages in the browser console
- Ensure all dependencies are properly installed
- Verify camera and microphone permissions
  
