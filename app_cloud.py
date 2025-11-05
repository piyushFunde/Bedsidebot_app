from flask import Flask, render_template, request, jsonify, send_from_directory
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
    return jsonify({"status": "healthy", "message": "BedsideBot is running"})

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
    if 'id' not in data:
        data['id'] = f"P{len(registration_data['patients']) + 1:03d}"
    data['lastActivity'] = 'Just registered'
    registration_data['patients'].append(data)
    return jsonify({"status": "success", "message": "Patient registered successfully", "patient_id": data['id']})

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print("[INFO] Starting BedsideBot Cloud Version...")
    print(f"[INFO] Server running on port: {port}")
    app.run(debug=False, host='0.0.0.0', port=port)