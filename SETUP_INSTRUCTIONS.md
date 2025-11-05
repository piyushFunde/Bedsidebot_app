# BedsideBot Patient Details & Print Report Setup

## Quick Setup Guide

### 1. Start the Application

```bash
# Navigate to the project directory
cd "c:\Users\Rahul Sunil Pharande\OneDrive\Desktop\Vercel\bedsidebot_final"

# Install dependencies (if not already installed)
pip install flask flask-sqlalchemy flask-cors python-dotenv

# Start the application
python app.py
```

### 2. Access the ICU Dashboard

Open your browser and navigate to:
```
http://localhost:8080/icu_dashboard
```

### 3. Add Sample Patients

Since you need patients to test the new features, you can either:

**Option A: Use the Patient Registration Form**
1. Go to `http://localhost:8080/patient`
2. Fill out the patient registration form
3. Submit to add patients to the database

**Option B: Add via the Registration Flow**
1. Start at `http://localhost:8080/`
2. Follow the complete registration process:
   - Hospital Registration
   - Staff Registration  
   - Patient Registration
   - Caregiver Registration

### 4. Test the New Features

Once you have patients in the system:

1. **View Patient Details**
   - Click on any patient card in the ICU Dashboard
   - Or click the "👁️ View Details" button
   - Browse through the organized patient information

2. **Generate Print Reports**
   - Click the "🖨️ Print Report" button on any patient card
   - Or use the print button in the patient details modal
   - The report will open in a new window with professional formatting

## Sample Patient Data

If you want to manually add a patient for testing, use these sample values in the patient registration form:

### Patient 1: John Smith
- **Patient Name**: John Smith
- **Patient ID**: P001
- **Date of Birth**: 1975-03-15
- **Gender**: Male
- **Blood Type**: A+
- **Primary Condition**: Post-surgical recovery
- **Mobility Level**: Limited Mobility
- **Medical History**: Appendectomy performed 2 days ago. History of hypertension, managed with medication.
- **Attending Physician**: Dr. Sarah Johnson
- **Admission Date**: Today's date
- **Room Number**: 101
- **Bed Number**: A
- **Department**: Intensive Care Unit (ICU)
- **Care Level**: Intensive Care
- **Assigned Nurse ID**: N001
- **Communication Methods**: Voice Commands, Hand Gestures, Facial Expressions
- **Communication Notes**: Patient prefers voice commands but can use gestures when tired. Speaks English fluently.

### Patient 2: Maria Garcia
- **Patient Name**: Maria Garcia
- **Patient ID**: P002
- **Date of Birth**: 1982-07-22
- **Gender**: Female
- **Blood Type**: O-
- **Primary Condition**: Cardiac monitoring
- **Mobility Level**: Moderate Care
- **Medical History**: Recent myocardial infarction. Stable condition.
- **Room Number**: 102
- **Bed Number**: B
- **Department**: Cardiology
- **Care Level**: Moderate Care
- **Communication Methods**: Voice Commands, Eye Tracking
- **Communication Notes**: Patient speaks Spanish primarily, some English.

## Features Overview

### Patient Details Modal
- **Trigger**: Click on patient card or "View Details" button
- **Content**: Complete patient information in organized sections
- **Actions**: Print report, close modal
- **Navigation**: Keyboard shortcuts (Escape to close)

### Print Report
- **Format**: Professional medical report in Times New Roman
- **Sections**: 
  - Patient Information
  - Medical Information  
  - Request Summary (30 days)
  - Recent Activity (20 requests)
  - Communication Preferences
- **Print Ready**: Optimized for standard paper sizes

### ICU Dashboard Enhancements
- **Interactive Cards**: Clickable patient cards with hover effects
- **Action Buttons**: View Details, Print Report, Remove Patient
- **Real-time Updates**: Live patient monitoring status
- **Responsive Design**: Works on desktop, tablet, and mobile

## Troubleshooting

### No Patients Showing
1. Make sure you've registered at least one patient
2. Check that the patient's status is "Active"
3. Refresh the ICU Dashboard page

### Print Report Not Working
1. Ensure your browser allows pop-ups
2. Check that the patient has required information filled out
3. Try using a different browser (Chrome recommended)

### Modal Not Opening
1. Check browser console for JavaScript errors
2. Ensure JavaScript is enabled
3. Try refreshing the page

## Technical Notes

### Database
- Patient data is stored in SQLite database (`bedsidebot.db`)
- All patient information is preserved between sessions
- Reports are generated dynamically from current data

### Security
- Input validation and sanitization
- SQL injection protection
- XSS prevention in reports
- Rate limiting on API endpoints

### Browser Compatibility
- **Recommended**: Chrome, Firefox, Safari, Edge
- **Not Supported**: Internet Explorer

## Next Steps

After testing the patient details and print report features:

1. **Explore Analytics**: Visit `/analytics` for system insights
2. **Test Monitoring**: Use `/interface` for patient interaction simulation
3. **Review Logs**: Check the activity log in the ICU Dashboard
4. **Customize**: Modify templates and styling as needed

## Support

For additional help:
1. Check the main README.md file
2. Review the PATIENT_DETAILS_GUIDE.md for detailed feature documentation
3. Contact the development team for technical support

---

**Important**: The new patient details and print report features are now fully integrated into the ICU Dashboard. They provide healthcare professionals with comprehensive patient information and professional reporting capabilities essential for quality patient care.