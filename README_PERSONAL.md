# My BedsideBot Healthcare System

This is my personal implementation and customization of the BedsideBot healthcare system - a multi-assistant patient care system that uses various recognition technologies to help bedridden and physically disabled patients communicate their needs effectively.

## 🚀 Features

- **Hand Sign Detection**: Finger gesture recognition (1-5 fingers) for patient needs selection
- **Voice Recognition**: Natural speech processing for voice commands
- **Emotion Detection**: Facial emotion analysis for patient monitoring
- **Eye Gaze Tracking**: Eye movement tracking for interface control
- **Multi-page Registration System**: Complete hospital, staff, patient, and caregiver registration
- **Real-time Monitoring**: Live patient monitoring with notification system
- **Analytics Dashboard**: Patient request patterns and healthcare analytics

## 🛠️ Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera for video processing
- Microphone for voice recognition (optional)

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/bedsidebot-healthcare-system.git
   cd bedsidebot-healthcare-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the system**
   - Open browser and go to `http://localhost:5000`
   - Start with registration process

## 📋 Usage Flow

1. **Registration Process**
   - Hospital Registration → Staff Registration → Patient Registration → Caregiver Registration → Module Selection

2. **Patient Monitoring**
   - Access Patient Interface → Enter patient details → Select recognition features → Start monitoring

3. **Recognition Methods**
   - **Hand Gestures**: 1-5 fingers for different needs
   - **Voice Commands**: "water", "food", "nurse", "bathroom", "emergency"
   - **Emotion Detection**: Automatic facial emotion analysis
   - **Eye Gaze**: Look directions for option selection

## 🏥 Patient Communication Options

1. **Call Nurse** - Request nursing assistance
2. **Water** - Request water or hydration
3. **Food** - Request food or meals
4. **Bathroom** - Request bathroom assistance
5. **Emergency** - Emergency alert system

## 🔧 Configuration

### Environment Variables (.env)
```
# Email Configuration
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
CAREGIVER_EMAIL=caregiver@hospital.com

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=+1234567890
CAREGIVER_PHONE=+0987654321

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## 📊 API Endpoints

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

## 🔒 Security & Privacy

- All patient data stored locally during sessions
- HIPAA compliance considerations included
- Secure environment variable management
- Rate limiting implemented

## 🚨 Troubleshooting

### Common Issues
1. **Camera not working**: Check webcam permissions and connections
2. **Voice recognition issues**: Verify microphone permissions
3. **Email/SMS not sending**: Check credentials in .env file
4. **Module import errors**: Reinstall dependencies with `pip install -r requirements.txt`

## 📝 License

This project is for educational and healthcare purposes. Ensure compliance with healthcare regulations (HIPAA, etc.) when deploying in production.

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements.

## 📞 Support

For issues or questions, please create an issue in this repository.

---

**Note**: This is a personal implementation based on the original BedsideBot concept. All modifications and customizations are my own work.