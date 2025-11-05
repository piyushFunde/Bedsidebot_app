# Patient Details & Print Report Feature Guide

## Overview

The BedsideBot ICU Dashboard now includes comprehensive patient details viewing and professional print report generation capabilities. This guide explains how to access and use these features.

## Features

### 1. Patient Details Modal
- **Access**: Click on any patient card in the ICU Dashboard or click the "👁️ View Details" button
- **Content**: Displays complete patient information organized in sections:
  - Personal Information (Name, ID, DOB, Gender, Blood Type, etc.)
  - Hospital Assignment (Room, Bed, Department, Care Level, etc.)
  - Medical Information (Condition, Mobility, Physician, Medical History)
  - Communication Preferences (Methods, Notes)

### 2. Print Report Feature
- **Access**: Click "🖨️ Print Report" button on patient cards or in the patient details modal
- **Format**: Professional medical report in Times New Roman font
- **Content**: Comprehensive patient report including:
  - Patient demographics and hospital assignment
  - Medical information and history
  - Request summary and statistics (last 30 days)
  - Recent activity log (last 20 requests)
  - Communication preferences

## How to Use

### Viewing Patient Details

1. **Navigate to ICU Dashboard**
   ```
   http://localhost:8080/icu_dashboard
   ```

2. **View Patient Details**
   - Click anywhere on a patient card, OR
   - Click the "👁️ View Details" button on a patient card

3. **Navigate the Details Modal**
   - View organized sections of patient information
   - Use the "🖨️ Print Report" button to generate a report
   - Click "Close" or press Escape to close the modal

### Generating Print Reports

1. **From Patient Card**
   - Click the "🖨️ Print Report" button directly on any patient card

2. **From Details Modal**
   - Open patient details first
   - Click the "🖨️ Print Report" button in the modal actions

3. **Print Process**
   - Report opens in a new browser window
   - Formatted for professional printing in Times New Roman
   - Click the "🖨️ Print Report" button in the report to print
   - Use browser's print function (Ctrl+P) for additional options

## Report Contents

### Patient Information Section
- Full name and patient ID
- Date of birth and calculated age
- Gender and blood type
- Room and bed assignment
- Department and care level
- Admission date and assigned nurse

### Medical Information Section
- Primary medical condition
- Mobility level assessment
- Attending physician
- Complete medical history
- Known allergies
- Current medications

### Request Summary Section (Last 30 Days)
- Total number of requests
- Emergency alerts count
- Average response time
- Breakdown by request type:
  - Call Nurse requests
  - Water requests
  - Food requests
  - Bathroom assistance
  - Emergency alerts

### Recent Activity Section
- Last 20 patient requests
- Date and time of each request
- Request type and method used
- Current status of each request

### Communication Preferences
- Preferred communication methods
- Special communication notes
- Language preferences or limitations

## Technical Implementation

### Backend API Endpoints

1. **Patient Details**
   ```
   GET /api/patient/details/<patient_id>
   ```
   Returns complete patient information in JSON format.

2. **Print Report**
   ```
   GET /api/patient/report/<patient_id>
   ```
   Returns HTML-formatted report ready for printing.

### Frontend Features

1. **Interactive Patient Cards**
   - Clickable cards with hover effects
   - Action buttons for View, Print, and Remove
   - Real-time status updates

2. **Modal System**
   - Responsive design for all screen sizes
   - Keyboard shortcuts (Escape to close)
   - Click-outside-to-close functionality

3. **Print Optimization**
   - CSS media queries for print formatting
   - Times New Roman font family
   - Proper page breaks and margins
   - Print-specific styling

## Sample Data Setup

To test the features with sample patients:

1. **Run the sample data script**
   ```bash
   python add_sample_patient.py
   ```

2. **Sample patients include**
   - John Smith (P001) - Post-surgical recovery
   - Maria Garcia (P002) - Cardiac monitoring  
   - Robert Johnson (P003) - Stroke recovery

## Keyboard Shortcuts

- **Escape**: Close any open modal or notification
- **Ctrl+P**: Print current report (when report window is active)

## Mobile Responsiveness

The patient details and print features are fully responsive:
- **Desktop**: Full grid layout with multiple columns
- **Tablet**: Adjusted grid with fewer columns
- **Mobile**: Single column layout with stacked action buttons

## Troubleshooting

### Common Issues

1. **Patient details not loading**
   - Check if patient exists in database
   - Verify patient_id is correct
   - Check browser console for errors

2. **Print report not generating**
   - Ensure patient has required data fields
   - Check server logs for errors
   - Verify browser allows pop-ups

3. **Modal not displaying properly**
   - Check browser compatibility
   - Ensure JavaScript is enabled
   - Clear browser cache if needed

### Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support
- **Internet Explorer**: Limited support (not recommended)

## Security Features

- Input validation and sanitization
- SQL injection protection
- XSS prevention in report generation
- Rate limiting on API endpoints
- Secure patient data handling

## Future Enhancements

Planned improvements include:
- PDF report generation
- Email report functionality
- Custom report templates
- Bulk patient operations
- Advanced filtering and search
- Real-time data synchronization

## Support

For technical support or feature requests:
1. Check the main README.md file
2. Review the troubleshooting section
3. Contact the development team
4. Submit issues through the project repository

---

**Note**: This feature requires patients to be registered through the patient registration system. Use the sample data script to quickly set up test patients for demonstration purposes.