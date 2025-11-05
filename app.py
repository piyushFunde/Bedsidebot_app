from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from flask_cors import CORS
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

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
def register_patient():
    data = request.json
    patient_data = {
        'id': data.get('patientId', f"P{len(registration_data['patients']) + 1:03d}"),
        'patientId': data.get('patientId'),
        'name': data.get('fullName'),
        'fullName': data.get('fullName'),
        'bed_number': data.get('bedNumber'),
        'bedNumber': data.get('bedNumber'),
        'roomNumber': data.get('roomNumber'),
        'primaryCondition': data.get('primaryCondition'),
        'lastActivity': 'Just registered'
    }
    
    registration_data['patients'].append(patient_data)
    return jsonify({"status": "success", "message": "Patient registered successfully", "patient_id": patient_data['id']})

@app.route('/api/register/caregiver', methods=['POST'])
def register_caregiver():
    data = request.json
    registration_data['caregivers'].append(data)
    return jsonify({"status": "success", "message": "Caregiver registered successfully"})

@app.route('/api/get_patients', methods=['GET'])
def get_patients():
    enhanced_patients = []
    for i, patient in enumerate(registration_data['patients']):
        enhanced_patient = patient.copy()
        enhanced_patient['id'] = enhanced_patient.get('id', f'P{i+1:03d}')
        enhanced_patient['lastActivity'] = enhanced_patient.get('lastActivity', 'No recent activity')
        enhanced_patients.append(enhanced_patient)
    return jsonify({"status": "success", "patients": enhanced_patients})

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