from flask import Flask, render_template, Response, request, jsonify, send_from_directory
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
    return render_template('staff.html')

@app.route('/patient')
def patient_registration():
    return render_template('patient.html')

@app.route('/caregiver')
def caregiver_registration():
    return render_template('caregiver.html')

@app.route('/modules')
def module_selection():
    return render_template('modules.html')

@app.route('/interface')
def patient_interface():
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
    registration_data['hospital'] = data
    return jsonify({"status": "success", "message": "Hospital registered successfully"})

@app.route('/api/register/staff', methods=['POST'])
def register_staff():
    data = request.json
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
    registration_data['caregivers'].append(data)
    return jsonify({"status": "success", "message": "Caregiver registered successfully"})

@app.route('/api/get_patients', methods=['GET'])
def get_patients():
    try:
        patients = Patient.query.filter_by(is_active=True).all()
        patient_list = []
        
        for patient in patients:
            patient_dict = patient.to_dict()
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    print("[INFO] Starting BedsideBot Cloud Version...")
    print(f"[INFO] Server running on port: {port}")
    app.run(debug=False, host='0.0.0.0', port=port)