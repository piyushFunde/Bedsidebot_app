import cv2
import mediapipe as mp
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from flask_cors import CORS
import threading
from collections import deque
import time
import speech_recognition as sr
import pyttsx3
import json
import os
import numpy as np
import base64
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Mediapipe Hand Detector with optimized settings
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=0  # Use lighter model for speed
)
mp_drawing = mp.solutions.drawing_utils

# Initialize face detector for basic face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variables
selected_button = None
detected_button = None
previous_button = None
last_selection_time = 0
SELECTION_BUFFER_TIME = 3.0  # 3 seconds buffer between selections
cap = None
engine = pyttsx3.init()

# Action mapping for notifications
action_mapping = {
    "1": "Call Nurse",
    "2": "Need Water", 
    "3": "Need Food",
    "4": "Need Bathroom Assistance",
    "5": "Emergency!"
}

# Button names
button_names = ["CALL NURSE", "WATER", "FOOD", "BATHROOM", "EMERGENCY"]

# Patient information with face encoding
patient_info = {"name": "", "bed_number": "", "face_encoding": None}
patient_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
patient_face_template = None
patient_trained = False

# Active features
active_features = set()

# Gesture buffer
gesture_buffer = deque(maxlen=20)

# Eye gaze tracking variables - optimized
gaze_buffer = deque(maxlen=10)  # Smaller buffer for speed
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Performance tracking
frame_count = 0
start_time = time.time()
fps = 0

# Registration data storage (in production, use a database)
registration_data = {
    'hospital': {},
    'staff': [],
    'patients': [],
    'caregivers': []
}

# ICU Dashboard data
latest_request = None
patient_requests = []

# === EMAIL Notification Function ===
def send_email_notification(subject, body):
    sender_email = os.getenv("EMAIL_SENDER")
    receiver_email = os.getenv("CAREGIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Demo mode - just log the notification
    if password == "demo_mode":
        print(f"📧 [DEMO] Email to {receiver_email}:")
        print(f"   Subject: {subject}")
        print(f"   Body: {body}")
        return

    if not all([sender_email, receiver_email, password]):
        print("❌ Email configuration missing")
        return

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Email error: {e}")

# === SMS Notification Function ===
def send_sms_notification(message_body):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    phone_number = os.getenv("CAREGIVER_PHONE")
    
    # Demo mode - just log the notification
    if account_sid == "demo_mode":
        print(f"📱 [DEMO] SMS to {phone_number}:")
        print(f"   Message: {message_body}")
        return
        
    try:
        client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        message = client.messages.create(
            body=message_body,
            from_=os.getenv("TWILIO_PHONE"),
            to=os.getenv("CAREGIVER_PHONE")
        )
        print(f"✅ SMS sent! SID: {message.sid}")
    except Exception as e:
        print(f"❌ SMS error: {e}")

# === Trigger Notifications if Needed ===
def notify_caregiver(action_text, patient_name="", bed_number=""):
    global latest_request, patient_requests
    
    subject = f"Patient Request: {action_text}"

    if patient_name and bed_number:
        body = f"Patient {patient_name} (Bed #{bed_number}) has requested: {action_text}. Please respond immediately."
    else:
        body = f"A patient has requested: {action_text}. Please respond immediately."

    # Store request for ICU Dashboard
    request_data = {
        'patientName': patient_name or 'Unknown Patient',
        'bedNumber': bed_number or 'N/A',
        'requestType': get_request_type_from_text(action_text),
        'actionText': action_text,
        'timestamp': time.time()
    }
    
    latest_request = request_data
    patient_requests.append(request_data)
    
    # Keep only last 50 requests
    if len(patient_requests) > 50:
        patient_requests = patient_requests[-50:]
    
    print(f"🚨 PATIENT REQUEST: {patient_name} ({bed_number}) - {action_text}")
    print(f"📊 Request stored for ICU Dashboard")

    send_email_notification(subject, body)
    send_sms_notification(body)

def get_request_type_from_text(action_text):
    """Convert action text to request type number"""
    action_lower = action_text.lower()
    if 'nurse' in action_lower or 'call' in action_lower:
        return 1
    elif 'water' in action_lower:
        return 2
    elif 'food' in action_lower:
        return 3
    elif 'bathroom' in action_lower:
        return 4
    elif 'emergency' in action_lower:
        return 5
    return 1  # Default to nurse call

# Function to detect eye gaze direction
def detect_eye_gaze(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    if len(eyes) == 0:
        return None

    largest_eye = max(eyes, key=lambda eye: eye[2] * eye[3])
    x, y, w, h = largest_eye

    eye_roi = gray[y:y + h, x:x + w]
    _, threshold = cv2.threshold(eye_roi, 70, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)

    if M["m00"] == 0:
        return None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    eye_center_x = w // 2

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(frame, (x + cx, y + cy), 2, (0, 0, 255), 3)

    if cx < eye_center_x - 5:
        return "left"
    elif cx > eye_center_x + 5:
        return "right"
    else:
        return "center"

# Function to get stable eye gaze direction
def get_stable_gaze():
    if not gaze_buffer:
        return None

    valid_gazes = [g for g in gaze_buffer if g is not None]
    if not valid_gazes:
        return None

    return max(set(valid_gazes), key=valid_gazes.count)

# Function to count raised fingers
def count_raised_fingers(hand_landmarks):
    if not hand_landmarks:
        return 0
    fingers_up = 0
    tips = [8, 12, 16, 20]
    base = [6, 10, 14, 18]

    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers_up += 1

    for tip, base_point in zip(tips, base):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base_point].y:
            fingers_up += 1

    return fingers_up

# Function to stabilize gesture recognition
def get_stable_gesture():
    if len(gesture_buffer) < 3:  # Need at least 3 readings
        return None
    
    # Get most common gesture from recent readings
    recent_gestures = list(gesture_buffer)[-10:]
    valid_gestures = [g for g in recent_gestures if 1 <= g <= 5]
    
    if not valid_gestures:
        return None
        
    # Return most frequent valid gesture
    gesture_counts = {}
    for g in valid_gestures:
        gesture_counts[g] = gesture_counts.get(g, 0) + 1
    
    # Only return if gesture appears at least 2 times
    max_gesture = max(gesture_counts, key=gesture_counts.get)
    if gesture_counts[max_gesture] >= 2:
        return max_gesture
    
    return None

# Function to check if detected face is the patient
def is_patient_face(face_roi):
    global patient_trained, patient_face_template
    
    if not patient_trained or patient_face_template is None:
        return True  # If no patient trained, allow all faces
    
    try:
        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        gray_face = cv2.resize(gray_face, (100, 100))
        
        # Use template matching for simple face comparison
        result = cv2.matchTemplate(gray_face, patient_face_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        
        # Higher value means better match (1.0 = perfect match)
        return max_val > 0.6  # Adjust threshold as needed
    except:
        return False

# Function to process camera feed and recognize gestures and eye gaze
def process_frame():
    global selected_button, cap, detected_button, previous_button, frame_count, start_time, fps, last_selection_time

    if cap is None or not cap.isOpened():
        return None

    ret, frame = cap.read()
    if not ret or frame is None:
        return None
    
    # Calculate FPS
    frame_count += 1
    if frame_count % 30 == 0:
        fps = 30 / (time.time() - start_time)
        start_time = time.time()

    # Keep standard resolution
    frame = cv2.resize(frame, (640, 480))
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process hand detection
    if "Hand Sign Detection" in active_features:
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                fingers_count = count_raised_fingers(hand_landmarks)
                gesture_buffer.append(fingers_count)
                
                # Show current finger count
                cv2.putText(frame, f'Fingers: {fingers_count}', (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            stable_gesture = get_stable_gesture()
            if stable_gesture and 1 <= stable_gesture <= 5:
                current_time = time.time()
                
                # Show detected gesture
                cv2.putText(frame, f'Gesture: {stable_gesture}', (10, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                # Check if enough time has passed since last selection
                if (current_time - last_selection_time) >= SELECTION_BUFFER_TIME:
                    selected_button = stable_gesture
                    detected_button = selected_button
                    
                    button_idx = detected_button - 1
                    action_text = button_names[button_idx] if 0 <= button_idx < len(
                        button_names) else "Unknown Request"
                    notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])
                    previous_button = detected_button
                    last_selection_time = current_time
                    
                    # Show selection confirmation
                    cv2.putText(frame, f'SELECTED: {action_text}', (10, 110), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Process eye gaze detection
    if "Eye Gaze Detection" in active_features:
        gaze_direction = detect_eye_gaze(frame)
        if gaze_direction:
            gaze_buffer.append(gaze_direction)
            stable_gaze = get_stable_gaze()

            if stable_gaze:
                cv2.putText(frame, f'Gaze: {stable_gaze}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                new_button = None
                if stable_gaze == "left":
                    new_button = 1
                elif stable_gaze == "right":
                    new_button = 5
                elif stable_gaze == "center":
                    new_button = 3

                if new_button is not None:
                    current_time = time.time()
                    
                    # Check if enough time has passed since last selection
                    if (current_time - last_selection_time) >= SELECTION_BUFFER_TIME:
                        selected_button = new_button
                        detected_button = selected_button
                        
                        button_idx = detected_button - 1
                        action_text = button_names[button_idx] if 0 <= button_idx < len(
                            button_names) else "Unknown Request"
                        notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])
                        previous_button = detected_button
                        last_selection_time = current_time

    # Add system info to frame
    cv2.putText(frame, f'FPS: {fps:.0f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Show buffer status
    current_time = time.time()
    time_since_last = current_time - last_selection_time
    if time_since_last < SELECTION_BUFFER_TIME:
        remaining = SELECTION_BUFFER_TIME - time_since_last
        cv2.putText(frame, f'Buffer: {remaining:.1f}s', (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    
    # Add patient info
    if patient_info.get('name'):
        cv2.putText(frame, f'Patient: {patient_info["name"]}', (10, frame.shape[0] - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame

# Generate frames for video streaming
def generate_frames():
    global cap
    
    # Initialize camera on first access
    if cap is None:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
    
    while True:
        if cap is None or not cap.isOpened():
            # Show error frame
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, 'Camera Not Started', (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'Click Start Monitoring', (120, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        else:
            frame = process_frame()
            if frame is None:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, 'Processing...', (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        time.sleep(0.033)

# Voice recognition function with trigger word
def voice_recognition():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)

        command = recognizer.recognize_google(audio).lower()
        
        # Simplified voice commands - no trigger word needed
        if "water" in command:
            return {"status": "success", "command": "water", "button": 2}
        elif "food" in command:
            return {"status": "success", "command": "food", "button": 3}
        elif "emergency" in command:
            return {"status": "success", "command": "emergency", "button": 5}
        elif "help" in command or "nurse" in command:
            return {"status": "success", "command": "help", "button": 1}
        elif "bathroom" in command or "toilet" in command:
            return {"status": "success", "command": "bathroom", "button": 4}
        else:
            return {"status": "no_command", "command": command}

    except sr.WaitTimeoutError:
        return {"status": "timeout"}
    except sr.UnknownValueError:
        return {"status": "no_speech"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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

@app.route('/icu_dashboard')
def icu_dashboard():
    return render_template('icu_dashboard.html')

@app.route('/icu_access')
def icu_access():
    return render_template('icu_access.html')

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
    # Add timestamp and ID to patient data
    data['registered_at'] = time.time()
    data['id'] = len(registration_data['patients']) + 1
    registration_data['patients'].append(data)
    return jsonify({"status": "success", "message": "Patient registered successfully"})

@app.route('/api/register/caregiver', methods=['POST'])
def register_caregiver():
    data = request.json
    registration_data['caregivers'].append(data)
    return jsonify({"status": "success", "message": "Caregiver registered successfully"})

# Existing monitoring routes
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/train_patient_face', methods=['POST'])
def train_patient_face():
    global patient_trained, patient_face_template, patient_info
    
    try:
        data = request.json
        image_data = data.get('image')
        
        # Decode base64 image
        image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64,
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale and detect face
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = patient_face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return jsonify({"status": "error", "message": "No face detected in image"})
        
        # Use the largest face as template
        (x, y, w, h) = max(faces, key=lambda face: face[2] * face[3])
        face_roi = gray[y:y+h, x:x+w]
        patient_face_template = cv2.resize(face_roi, (100, 100))
        patient_trained = True
        
        return jsonify({"status": "success", "message": "Patient face trained successfully"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global active_features, patient_info, cap

    data = request.json
    patient_info = {
        "name": data.get("patientName", ""),
        "bed_number": data.get("bedNumber", ""),
        "face_encoding": None
    }
    active_features = set(data.get("features", []))
    
    print(f"Starting monitoring for patient: {patient_info['name']} in bed: {patient_info['bed_number']}")
    print(f"Active features: {active_features}")

    # Initialize camera
    if cap is None:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)

    return jsonify({"status": "success", "message": "Monitoring started", "patient": patient_info})

@app.route('/get_selected_button')
def get_selected_button():
    global detected_button, previous_button, selected_button, last_selection_time

    current_button = selected_button
    current_time = time.time()
    time_since_last = current_time - last_selection_time

    if current_button is not None:
        button_idx = current_button - 1
        button_text = button_names[button_idx] if 0 <= button_idx < len(button_names) else "Unknown Request"
        
        return jsonify({
            "button": current_button, 
            "text": button_text,
            "time_remaining": max(0, SELECTION_BUFFER_TIME - time_since_last)
        })

    return jsonify({
        "button": None, 
        "text": "None",
        "time_remaining": max(0, SELECTION_BUFFER_TIME - time_since_last)
    })

@app.route('/set_button', methods=['POST'])
def set_button():
    global detected_button, previous_button

    data = request.get_json()
    button = data.get("button")

    if button != detected_button:
        detected_button = button

        if detected_button is not None and detected_button != previous_button:
            if isinstance(detected_button, str) and detected_button.isdigit():
                detected_button = int(detected_button)

            if isinstance(detected_button, int) and 1 <= detected_button <= 5:
                button_idx = detected_button - 1
                action_text = button_names[button_idx]
                notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])
            else:
                action_text = action_mapping.get(detected_button, "Unknown Request")
                notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])

            previous_button = detected_button

    return jsonify({"status": "success"})

@app.route('/listen_voice', methods=['POST'])
def listen_voice():
    global detected_button, previous_button, last_selection_time, selected_button

    if "Voice Recognition" not in active_features:
        return jsonify({"status": "error", "message": "Voice recognition not active"})

    current_time = time.time()
    
    # Check buffer only for successful commands
    result = voice_recognition()

    if result.get("status") == "success" and result.get("button"):
        # Check if enough time has passed since last selection
        if (current_time - last_selection_time) >= SELECTION_BUFFER_TIME:
            button = result.get("button")
            
            selected_button = button
            detected_button = button
            button_idx = detected_button - 1
            action_text = button_names[button_idx] if 0 <= button_idx < len(button_names) else "Unknown Request"
            notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])
            previous_button = detected_button
            last_selection_time = current_time
        else:
            time_remaining = SELECTION_BUFFER_TIME - (current_time - last_selection_time)
            result["status"] = "buffer_active"
            result["message"] = f"Wait {time_remaining:.1f}s before next selection"

    return jsonify(result)

@app.route('/get_active_features')
def get_active_features():
    return jsonify({
        "features": list(active_features),
        "patientName": patient_info.get("name", ""),
        "bedNumber": patient_info.get("bed_number", "")
    })

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global cap, active_features, detected_button, previous_button, last_selection_time

    if cap is not None:
        cap.release()
        cap = None

    active_features.clear()
    detected_button = None
    previous_button = None
    last_selection_time = 0

    return jsonify({"status": "success", "message": "Monitoring stopped"})

# ICU Dashboard API endpoints
@app.route('/api/get_patients')
def get_patients():
    """Get list of registered patients for ICU dashboard"""
    patients_list = []
    print(f"Total registered patients: {len(registration_data['patients'])}")
    
    for i, patient in enumerate(registration_data['patients']):
        patient_data = {
            'id': patient.get('id', i + 1),
            'name': patient.get('fullName', 'Unknown'),
            'bed_number': patient.get('bedNumber', 'N/A'),
            'room_number': patient.get('roomNumber', 'N/A'),
            'department': patient.get('department', 'N/A'),
            'condition': patient.get('primaryCondition', 'N/A'),
            'lastActivity': 'No recent activity'
        }
        patients_list.append(patient_data)
        print(f"Patient {i+1}: {patient_data['name']} - Bed: {patient_data['bed_number']}")
    
    return jsonify({'patients': patients_list, 'total': len(patients_list)})

@app.route('/api/get_latest_request')
def get_latest_request():
    """Get the latest patient request for ICU dashboard"""
    global latest_request
    
    if latest_request:
        # Check if request is recent (within last 10 seconds)
        if time.time() - latest_request['timestamp'] < 10:
            request_to_send = latest_request
            latest_request = None  # Clear after sending
            print(f"📱 Sending request to ICU Dashboard: {request_to_send}")
            return jsonify({'request': request_to_send})
    
    return jsonify({'request': None})

@app.route('/api/get_all_requests')
def get_all_requests():
    """Get all patient requests for ICU dashboard"""
    return jsonify({'requests': patient_requests})

# Clean up resources when the app is shutting down
def cleanup():
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()

# Add route to check camera status
@app.route('/camera_status')
def camera_status():
    global cap
    status = {
        'camera_available': cap is not None and cap.isOpened(),
        'active_features': list(active_features),
        'patient_info': patient_info
    }
    return jsonify(status)

# Simple camera test route
@app.route('/camera_test')
def camera_test():
    return '''<!DOCTYPE html>
<html>
<head><title>Camera Test</title></head>
<body style="text-align: center; padding: 50px;">
    <h1>Camera Test</h1>
    <img src="/video_feed" style="border: 2px solid #333; max-width: 640px; width: 100%;">
    <p>If you can see yourself above, the camera is working!</p>
    <a href="/interface">Go to Patient Interface</a>
</body>
</html>'''

if __name__ == "__main__":
    try:
        print("BedsideBot - Starting System...")
        print("Open your browser to: http://localhost:5000")
        print("Press Ctrl+C to stop the application")
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    finally:
        cleanup()