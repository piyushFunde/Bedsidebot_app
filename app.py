from flask import Flask, render_template, Response, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import json
import os
from datetime import datetime, date
from dotenv import load_dotenv
from security import security, require_auth, validate_patient_data, sanitize_patient_data, log_security_event
from database import db, init_database, Hospital, Staff, Patient, PatientRequest, MonitoringSession, Caregiver, SystemAnalytics, get_patient_request_patterns
from analytics_routes import analytics_bp

# Load environment variables
load_dotenv()

# Initialize Flask app with security
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bedsidebot.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins=['https://*.railway.app', 'https://localhost:*'])

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Initialize database
init_database(app)

# Register analytics blueprint
app.register_blueprint(analytics_bp)

# Registration data storage
registration_data = {
    'hospital': {},
    'staff': [],
    'patients': [],
    'caregivers': []
}

# Latest request storage
latest_request = None
selected_button = None
detected_button = None
previous_button = None

# Patient information
patient_info = {"name": "", "bed_number": ""}

# Active features
active_features = set()

# Routes for the multi-page frontend
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/hospital')
def hospital_registration():
    return render_template('hospital.html')

@app.route('/staff')
def staff_registration():
    # Check if hospital registration is completed
    if not registration_data.get('hospital'):
        return redirect('/hospital')
    return render_template('staff.html')

@app.route('/patient')
def patient_registration():
    # Check if previous steps are completed
    if not registration_data.get('hospital') or not registration_data.get('staff'):
        return redirect('/hospital')
    return render_template('patient.html')

@app.route('/caregiver')
def caregiver_registration():
    # Check if previous steps are completed
    if not registration_data.get('hospital') or not registration_data.get('staff') or not registration_data.get('patients'):
        return redirect('/hospital')
    return render_template('caregiver.html')

@app.route('/modules')
def module_selection():
    return render_template('modules.html')

@app.route('/interface')
def patient_interface():
    return render_template('interface.html')

@app.route('/interface/<patient_id>')
def patient_interface_specific(patient_id):
    # Get patient info for specific interface
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        return render_template('interface.html', patient=patient.to_dict())
    return render_template('interface.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/icu_access')
def icu_access():
    return render_template('icu_access.html')

@app.route('/icu_dashboard')
def icu_dashboard():
    return render_template('icu_dashboard.html')

@app.route('/analytics')
def analytics_dashboard():
    return render_template('analytics_dashboard.html')

@app.route('/static/<filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Health check endpoint
@app.route('/health')
def health_check():
    return "OK", 200

# Browser camera access page
@app.route('/camera')
def camera_access():
    return render_template('camera.html')

# Video feed endpoint (browser camera access)
@app.route('/video_feed')
def video_feed():
    return '''
    <html><body style="text-align: center; padding: 50px; font-family: Arial;">
    <h2>🎥 Camera Access Required</h2>
    <p>Please use the <a href="/camera">Camera Interface</a> for live video.</p>
    </body></html>
    '''

# API Routes for registration
@app.route('/api/register/hospital', methods=['POST'])
def register_hospital():
    data = request.json
    # Validate required fields
    required_fields = ['hospitalName', 'hospitalId', 'fullAddress', 'city', 'state', 'zipCode', 'primaryPhone', 'email', 'adminName', 'licenseNumber', 'totalBeds', 'icuBeds']
    
    for field in required_fields:
        if not data.get(field):
            return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
    
    registration_data['hospital'] = data
    return jsonify({"status": "success", "message": "Hospital registered successfully"})

@app.route('/api/register/staff', methods=['POST'])
def register_staff():
    data = request.json
    # Validate required fields
    required_fields = ['fullName', 'employeeId', 'role', 'department', 'shift', 'phoneNumber', 'email', 'experience', 'startDate', 'employmentStatus', 'accessLevel', 'notifications']
    
    for field in required_fields:
        if not data.get(field):
            return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
    
    registration_data['staff'].append(data)
    return jsonify({"status": "success", "message": "Staff registered successfully"})

@app.route('/api/register/patient', methods=['POST'])
@limiter.limit("5 per minute")
def register_patient():
    data = request.json
    
    # Security validation
    validation_errors = validate_patient_data(data)
    if validation_errors:
        log_security_event('INVALID_INPUT', f'Patient registration validation failed: {validation_errors}')
        return jsonify({'error': 'Invalid input data', 'details': validation_errors}), 400
    
    # Sanitize data
    sanitized_data = sanitize_patient_data(data)
    
    patient_data = {
        'id': sanitized_data.get('patientId', f"P{len(registration_data['patients']) + 1:03d}"),
        'patientId': sanitized_data.get('patientId'),
        'name': sanitized_data.get('fullName'),
        'fullName': sanitized_data.get('fullName'),
        'bed_number': sanitized_data.get('bedNumber'),
        'bedNumber': sanitized_data.get('bedNumber'),
        'roomNumber': sanitized_data.get('roomNumber'),
        'primaryCondition': sanitized_data.get('primaryCondition'),
        'lastActivity': 'Just registered'
    }
    
    # Save to database
    try:
        new_patient = Patient(
            patient_id=sanitized_data.get('patientId'),
            full_name=sanitized_data.get('fullName'),
            date_of_birth=datetime.strptime(sanitized_data.get('dateOfBirth'), '%Y-%m-%d').date() if sanitized_data.get('dateOfBirth') else None,
            gender=sanitized_data.get('gender'),
            blood_type=sanitized_data.get('bloodType'),
            primary_condition=sanitized_data.get('primaryCondition'),
            mobility_level=sanitized_data.get('mobilityLevel'),
            medical_history=sanitized_data.get('medicalHistory'),
            attending_physician=sanitized_data.get('attendingPhysician'),
            room_number=sanitized_data.get('roomNumber'),
            bed_number=sanitized_data.get('bedNumber'),
            department=sanitized_data.get('department'),
            care_level=sanitized_data.get('careLevel'),
            assigned_nurse_id=sanitized_data.get('assignedNurse'),
            communication_methods=json.dumps(sanitized_data.get('communicationMethods', [])),
            communication_notes=sanitized_data.get('communicationNotes'),
            admission_date=datetime.strptime(sanitized_data.get('admissionDate'), '%Y-%m-%d').date() if sanitized_data.get('admissionDate') else date.today()
        )
        
        db.session.add(new_patient)
        db.session.commit()
        
        # Also keep in memory for backward compatibility
        registration_data['patients'].append(patient_data)
        
        # Ensure patients list exists for validation
        if not registration_data.get('patients'):
            registration_data['patients'] = []
        
        log_security_event('PATIENT_REGISTERED', f'Patient {new_patient.full_name} registered successfully')
        
        return jsonify({
            "status": "success", 
            "message": "Patient registered successfully", 
            "patient_id": new_patient.patient_id
        })
        
    except Exception as e:
        db.session.rollback()
        log_security_event('PATIENT_REGISTRATION_ERROR', f'Database error: {str(e)}')
        return jsonify({"status": "error", "message": "Registration failed. Please try again."}), 500

@app.route('/api/register/caregiver', methods=['POST'])
def register_caregiver():
    data = request.json
    # Validate required fields
    required_fields = ['fullName', 'caregiverId', 'relationship', 'primaryPhone', 'email', 'accessLevel', 'notifications', 'contactMethod', 'decisionMaking', 'availability']
    
    for field in required_fields:
        if not data.get(field):
            return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
    
    registration_data['caregivers'].append(data)
    return jsonify({"status": "success", "message": "Caregiver registered successfully"})

@app.route('/api/get_patients', methods=['GET'])
def get_patients():
    try:
        patients = Patient.query.filter_by(is_active=True).all()
        patient_list = []
        
        for patient in patients:
            patient_dict = patient.to_dict()
            # Add compatibility fields for dashboard
            patient_dict['id'] = patient.patient_id
            patient_dict['name'] = patient.full_name
            
            # Add last activity from recent requests
            recent_request = PatientRequest.query.filter_by(patient_id=patient.patient_id).order_by(PatientRequest.timestamp.desc()).first()
            patient_dict['lastActivity'] = recent_request.timestamp.strftime('%Y-%m-%d %H:%M') if recent_request else 'No recent activity'
            patient_list.append(patient_dict)
        
        return jsonify({"status": "success", "patients": patient_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/get_latest_request', methods=['GET'])
def get_latest_request():
    global latest_request
    if latest_request:
        request_data = latest_request
        latest_request = None
        return jsonify({"request": request_data})
    return jsonify({"request": None})

@app.route('/api/remove_patient', methods=['POST'])
def remove_patient():
    data = request.json
    patient_id = data.get('patient_id')
    registration_data['patients'] = [p for p in registration_data['patients'] if p.get('id') != patient_id]
    return jsonify({"status": "success", "message": "Patient removed from monitoring"})

# Monitoring routes (simplified for cloud)
@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global active_features, patient_info
    data = request.json
    # Get patient from registered patients
    patients = registration_data.get('patients', [])
    if patients:
        patient = patients[0]
        patient_info = {
            "name": patient.get("fullName", data.get("patientName", "")),
            "id": patient.get("patientId", "N/A"),
            "bed_number": patient.get("bedNumber", data.get("bedNumber", "")),
            "room_number": patient.get("roomNumber", "N/A"),
            "primary_condition": patient.get("primaryCondition", "N/A")
        }
    else:
        patient_info = {
            "name": data.get("patientName", ""),
            "id": "N/A",
            "bed_number": data.get("bedNumber", ""),
            "room_number": "N/A",
            "primary_condition": "N/A"
        }
    active_features = set(data.get("features", []))
    return jsonify({"status": "success", "message": "Monitoring started (cloud mode)"})

@app.route('/get_selected_button')
def get_selected_button():
    global selected_button
    # Simulate button detection for demo
    return jsonify({"button": selected_button, "text": "Demo Mode"})

@app.route('/set_button', methods=['POST'])
def set_button():
    global selected_button, latest_request
    data = request.get_json()
    button = data.get("button")
    
    if button and 1 <= button <= 5:
        selected_button = button
        button_names = ["Call Nurse", "Water", "Food", "Bathroom", "Emergency"]
        action_name = button_names[button - 1]
        
        # Save request to database
        try:
            new_request = PatientRequest(
                patient_id=patient_info.get("id", "UNKNOWN"),
                request_type=button,
                request_method='gesture',
                request_message=f"Hand Gesture: {action_name}",
                room_number=patient_info.get("room_number", "N/A"),
                bed_number=patient_info.get("bed_number", "N/A"),
                urgency_level='critical' if button == 5 else 'normal'
            )
            
            db.session.add(new_request)
            db.session.commit()
            
        except Exception as e:
            print(f"[ERROR] Failed to save request: {e}")
        
        # Update latest request for real-time dashboard
        latest_request = {
            "patientName": patient_info.get("name", "Unknown Patient"),
            "patientId": patient_info.get("id", "N/A"),
            "bedNumber": patient_info.get("bed_number", "N/A"),
            "roomNumber": patient_info.get("room_number", "N/A"),
            "primaryCondition": patient_info.get("primary_condition", "N/A"),
            "requestType": button,
            "timestamp": time.time(),
            "message": f"Hand Gesture: {action_name}",
            "type": "gesture"
        }
        
        print(f"[NOTIFICATION] {patient_info.get('name', 'Patient')} - {action_name} (Gesture)")
        return jsonify({"status": "success", "message": action_name})
    
    return jsonify({"status": "error", "message": "Invalid gesture"})

@app.route('/listen_voice', methods=['POST'])
def listen_voice():
    # Simulate voice recognition for demo
    return jsonify({"status": "ready", "message": "Voice recognition ready (cloud mode)"})

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global active_features, selected_button
    active_features.clear()
    selected_button = None
    return jsonify({"status": "success", "message": "Monitoring stopped"})

@app.route('/api/patient/details/<patient_id>', methods=['GET'])
def get_patient_details(patient_id):
    """Get detailed patient information"""
    try:
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if not patient:
            return jsonify({'status': 'error', 'message': 'Patient not found'}), 404
        
        return jsonify({
            'status': 'success',
            'patient': patient.to_dict()
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/patient/report/<patient_id>', methods=['GET'])
def generate_patient_report(patient_id):
    """Generate comprehensive patient report"""
    try:
        # Get patient data
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if not patient:
            return jsonify({'status': 'error', 'message': 'Patient not found'}), 404
        
        # Get patient requests (last 30 days)
        from datetime import timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        requests = PatientRequest.query.filter(
            PatientRequest.patient_id == patient_id,
            PatientRequest.timestamp >= thirty_days_ago
        ).order_by(PatientRequest.timestamp.desc()).all()
        
        # Get request patterns
        patterns = get_patient_request_patterns(patient_id, 30)
        
        # Generate HTML report
        report_html = generate_report_html(patient, requests, patterns)
        
        return jsonify({
            'status': 'success',
            'report': report_html
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def generate_report_html(patient, requests, patterns):
    """Generate HTML report for printing"""
    
    # Calculate age
    age = 'N/A'
    if patient.date_of_birth:
        today = date.today()
        age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))
    
    # Request type names
    request_types = {
        1: 'Call Nurse',
        2: 'Water Request', 
        3: 'Food Request',
        4: 'Bathroom Assistance',
        5: 'Emergency Alert'
    }
    
    # Generate request summary
    request_summary = []
    for req_type, count in patterns.get('request_types', {}).items():
        request_summary.append(f"{request_types.get(req_type, 'Unknown')}: {count} times")
    
    # Recent requests table
    recent_requests_html = ''
    for req in requests[:20]:  # Last 20 requests
        recent_requests_html += f'''
        <tr>
            <td>{req.timestamp.strftime('%Y-%m-%d %H:%M')}</td>
            <td>{request_types.get(req.request_type, 'Unknown')}</td>
            <td>{req.request_method.title()}</td>
            <td>{req.status.title()}</td>
        </tr>
        '''
    
    report_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Patient Report - {patient.full_name}</title>
        <style>
            @media print {{
                body {{ margin: 0; }}
                .no-print {{ display: none; }}
            }}
            body {{
                font-family: "Times New Roman", serif;
                font-size: 12pt;
                line-height: 1.4;
                margin: 20px;
                color: #000;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #000;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .hospital-name {{
                font-size: 18pt;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .report-title {{
                font-size: 16pt;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .report-date {{
                font-size: 10pt;
                color: #666;
            }}
            .section {{
                margin-bottom: 20px;
                page-break-inside: avoid;
            }}
            .section-title {{
                font-size: 14pt;
                font-weight: bold;
                border-bottom: 1px solid #000;
                padding-bottom: 3px;
                margin-bottom: 10px;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 15px;
            }}
            .info-item {{
                margin-bottom: 8px;
            }}
            .label {{
                font-weight: bold;
                display: inline-block;
                width: 150px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f0f0f0;
                font-weight: bold;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin: 15px 0;
            }}
            .stat-box {{
                border: 1px solid #000;
                padding: 10px;
                text-align: center;
            }}
            .stat-number {{
                font-size: 18pt;
                font-weight: bold;
                color: #000;
            }}
            .stat-label {{
                font-size: 10pt;
                margin-top: 5px;
            }}
            .print-btn {{
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12pt;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 10px;
                border-top: 1px solid #000;
                font-size: 10pt;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="hospital-name">BedsideBot Healthcare System</div>
            <div class="report-title">Patient Monitoring Report</div>
            <div class="report-date">Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <button class="print-btn no-print" onclick="window.print()">🖨️ Print Report</button>
        
        <div class="section">
            <div class="section-title">Patient Information</div>
            <div class="info-grid">
                <div>
                    <div class="info-item"><span class="label">Full Name:</span> {patient.full_name}</div>
                    <div class="info-item"><span class="label">Patient ID:</span> {patient.patient_id}</div>
                    <div class="info-item"><span class="label">Date of Birth:</span> {patient.date_of_birth.strftime('%B %d, %Y') if patient.date_of_birth else 'N/A'}</div>
                    <div class="info-item"><span class="label">Age:</span> {age} years</div>
                    <div class="info-item"><span class="label">Gender:</span> {patient.gender or 'N/A'}</div>
                    <div class="info-item"><span class="label">Blood Type:</span> {patient.blood_type or 'N/A'}</div>
                </div>
                <div>
                    <div class="info-item"><span class="label">Room Number:</span> {patient.room_number}</div>
                    <div class="info-item"><span class="label">Bed Number:</span> {patient.bed_number}</div>
                    <div class="info-item"><span class="label">Department:</span> {patient.department}</div>
                    <div class="info-item"><span class="label">Care Level:</span> {patient.care_level}</div>
                    <div class="info-item"><span class="label">Admission Date:</span> {patient.admission_date.strftime('%B %d, %Y') if patient.admission_date else 'N/A'}</div>
                    <div class="info-item"><span class="label">Assigned Nurse:</span> {patient.assigned_nurse_id or 'N/A'}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Medical Information</div>
            <div class="info-item"><span class="label">Primary Condition:</span> {patient.primary_condition}</div>
            <div class="info-item"><span class="label">Mobility Level:</span> {patient.mobility_level or 'N/A'}</div>
            <div class="info-item"><span class="label">Attending Physician:</span> {patient.attending_physician or 'N/A'}</div>
            {f'<div class="info-item"><span class="label">Medical History:</span> {patient.medical_history}</div>' if patient.medical_history else ''}
            {f'<div class="info-item"><span class="label">Allergies:</span> {patient.allergies}</div>' if hasattr(patient, 'allergies') and patient.allergies else ''}
            {f'<div class="info-item"><span class="label">Current Medications:</span> {patient.current_medications}</div>' if hasattr(patient, 'current_medications') and patient.current_medications else ''}
        </div>
        
        <div class="section">
            <div class="section-title">Request Summary (Last 30 Days)</div>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-number">{patterns.get('total_requests', 0)}</div>
                    <div class="stat-label">Total Requests</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len([r for r in requests if r.request_type == 5])}</div>
                    <div class="stat-label">Emergency Alerts</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{round(sum(patterns.get('response_times', [0])) / len(patterns.get('response_times', [1])), 1) if patterns.get('response_times') else 0}</div>
                    <div class="stat-label">Avg Response (min)</div>
                </div>
            </div>
            
            <div style="margin-top: 15px;">
                <strong>Request Breakdown:</strong><br>
                {'; '.join(request_summary) if request_summary else 'No requests in the last 30 days'}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Recent Activity (Last 20 Requests)</div>
            <table>
                <thead>
                    <tr>
                        <th>Date & Time</th>
                        <th>Request Type</th>
                        <th>Method</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {recent_requests_html if recent_requests_html else '<tr><td colspan="4" style="text-align: center;">No recent requests</td></tr>'}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">Communication Preferences</div>
            <div class="info-item"><span class="label">Preferred Methods:</span> {', '.join(json.loads(patient.communication_methods)) if patient.communication_methods else 'Not specified'}</div>
            {f'<div class="info-item"><span class="label">Communication Notes:</span> {patient.communication_notes}</div>' if patient.communication_notes else ''}
        </div>
        
        <div class="footer">
            <p>This report was generated by BedsideBot Healthcare System</p>
            <p>For questions or concerns, please contact the nursing station</p>
        </div>
    </body>
    </html>
    '''
    
    return report_html

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    print("[INFO] Starting BedsideBot Cloud Version...")
    print(f"[INFO] Server running on port: {port}")
    app.run(debug=False, host='0.0.0.0', port=port)