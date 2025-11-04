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
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception as e:
    print(f"[WARNING] DeepFace not available: {e}")
    print("[INFO] Emotion detection will be disabled")
    DEEPFACE_AVAILABLE = False
    DeepFace = None

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except Exception as e:
    print(f"[WARNING] Twilio not available: {e}")
    TWILIO_AVAILABLE = False
    Client = None
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Mediapipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize face detector for emotion detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variables
selected_button = None
detected_button = None
previous_button = None
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

# Patient information
patient_info = {"name": "", "bed_number": ""}

# Active features
active_features = set()

# Gesture buffer
gesture_buffer = deque(maxlen=20)

# Eye gaze tracking variables
gaze_buffer = deque(maxlen=30)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Emotion to command mapping
emotion_to_command = {
    'angry': {'name': 'Anger', 'command': 'Patient is frustrated, needs assistance or calm down'},
    'disgust': {'name': 'Disgust', 'command': 'Patient is uncomfortable, needs hygiene or cleaning supplies'},
    'fear': {'name': 'Fear', 'command': 'Patient feels anxious, needs comfort or reassurance'},
    'happy': {'name': 'Happiness', 'command': 'Patient is comfortable, no immediate action needed'},
    'sad': {'name': 'Sadness', 'command': 'Patient is feeling down, may need emotional support or medication'},
    'surprise': {'name': 'Surprise', 'command': 'Patient is startled, check if there is an emergency or sudden change'},
    'neutral': {'name': 'Neutral', 'command': 'Patient is calm, routine check-up may be needed'}
}

# Registration data storage (in production, use a database)
registration_data = {
    'hospital': {},
    'staff': [],
    'patients': [],
    'caregivers': []
}

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
    if not TWILIO_AVAILABLE:
        print(f"[INFO] SMS notification (Twilio disabled): {message_body}")
        return
        
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    phone_number = os.getenv("CAREGIVER_PHONE")
    
    # Demo mode - just log the notification
    if account_sid == "demo_mode":
        print(f"[DEMO] SMS to {phone_number}: {message_body}")
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
        print(f"[OK] SMS sent! SID: {message.sid}")
    except Exception as e:
        print(f"[ERROR] SMS error: {e}")

# === Trigger Notifications if Needed ===
def notify_caregiver(action_text, patient_name="", bed_number=""):
    subject = f"Patient Request: {action_text}"

    if patient_name and bed_number:
        body = f"Patient {patient_name} (Bed #{bed_number}) has requested: {action_text}. Please respond immediately."
    else:
        body = f"A patient has requested: {action_text}. Please respond immediately."

    send_email_notification(subject, body)
    send_sms_notification(body)

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
    if not gesture_buffer:
        return None
    return max(set(gesture_buffer), key=gesture_buffer.count)

# Function to process camera feed and recognize gestures, emotions, and eye gaze
def process_frame():
    global selected_button, cap, detected_button, previous_button

    if cap is None or not cap.isOpened():
        return None

    ret, frame = cap.read()
    if not ret:
        return None

    # Flip the frame for better user experience
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hand detection
    if "Hand Sign Detection" in active_features:
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers_count = count_raised_fingers(hand_landmarks)
                gesture_buffer.append(fingers_count)

            stable_gesture = get_stable_gesture()
            if stable_gesture:
                selected_button = stable_gesture if 1 <= stable_gesture <= 5 else None

                if selected_button != detected_button:
                    detected_button = selected_button

                    if detected_button is not None and detected_button != previous_button:
                        button_idx = detected_button - 1
                        action_text = button_names[button_idx] if 0 <= button_idx < len(
                            button_names) else "Unknown Request"
                        notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])
                        previous_button = detected_button

    # Process emotion detection
    if "Emotion Detection" in active_features and DEEPFACE_AVAILABLE:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]

            try:
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

                dominant_emotion = result[0]['dominant_emotion']
                emotion = emotion_to_command.get(dominant_emotion, {'name': 'Unknown', 'command': 'Unknown emotion'})
                emotion_name = emotion['name']
                command = emotion['command']

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f'Patient: {patient_info["name"]}', (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                            (0, 255, 0), 2)
                cv2.putText(frame, f'Emotion: {emotion_name}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0),
                            2)

                if dominant_emotion in ['fear', 'angry', 'surprise']:
                    if detected_button != 5:
                        detected_button = 5
                        if detected_button != previous_button:
                            notify_caregiver(f"EMERGENCY: Patient showing {emotion_name}",
                                             patient_info["name"], patient_info["bed_number"])
                            previous_button = detected_button

            except Exception as e:
                print(f"Error in emotion detection: {e}")

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
                    selected_button = new_button

                    if selected_button != detected_button:
                        detected_button = selected_button

                        if detected_button != previous_button:
                            button_idx = detected_button - 1
                            action_text = button_names[button_idx] if 0 <= button_idx < len(
                                button_names) else "Unknown Request"
                            notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])
                            previous_button = detected_button

    return frame

# Generate frames for video streaming
def generate_frames():
    while True:
        frame = process_frame()
        if frame is None:
            continue

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        # Control frame rate
        time.sleep(0.1)

# Voice recognition function
def voice_recognition():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)

        command = recognizer.recognize_google(audio).lower()

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
            return {"status": "unknown", "command": command}

    except sr.WaitTimeoutError:
        return {"status": "timeout"}
    except sr.UnknownValueError:
        return {"status": "error", "message": "Could not understand audio"}
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

@app.route('/test_video')
def test_video():
    return render_template('test_video.html')

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
    registration_data['patients'].append(data)
    return jsonify({"status": "success", "message": "Patient registered successfully"})

@app.route('/api/register/caregiver', methods=['POST'])
def register_caregiver():
    data = request.json
    registration_data['caregivers'].append(data)
    return jsonify({"status": "success", "message": "Caregiver registered successfully"})

@app.route('/api/get_patients', methods=['GET'])
def get_patients():
    return jsonify({"status": "success", "patients": registration_data['patients']})

# Existing monitoring routes
@app.route('/video_feed')
def video_feed():
    print("[INFO] Video feed requested")
    try:
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"[ERROR] Video feed error: {e}")
        return str(e), 500

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global active_features, patient_info, cap

    data = request.json
    patient_info = {
        "name": data.get("patientName", ""),
        "bed_number": data.get("bedNumber", "")
    }
    active_features = set(data.get("features", []))

    # Initialize camera if needed
    if cap is None:
        cap = cv2.VideoCapture(0)
        print("[INFO] Camera initialized")

    # Return success message
    return jsonify({"status": "success", "message": "Monitoring started"})

@app.route('/get_selected_button')
def get_selected_button():
    global detected_button, previous_button, selected_button

    current_button = selected_button

    if current_button is not None:
        button_idx = current_button - 1
        button_text = button_names[button_idx] if 0 <= button_idx < len(button_names) else "Unknown Request"

        if current_button != detected_button:
            detected_button = current_button

            if detected_button != previous_button:
                notify_caregiver(button_text, patient_info["name"], patient_info["bed_number"])
                previous_button = detected_button

        return jsonify({"button": current_button, "text": button_text})

    return jsonify({"button": None, "text": "None"})

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
    global detected_button, previous_button

    if "Voice Recognition" not in active_features:
        return jsonify({"status": "error", "message": "Voice recognition not active"})

    result = voice_recognition()

    if result.get("status") == "success" and result.get("button"):
        button = result.get("button")

        if button != detected_button:
            detected_button = button

            if detected_button != previous_button:
                button_idx = detected_button - 1
                action_text = button_names[button_idx] if 0 <= button_idx < len(button_names) else "Unknown Request"
                notify_caregiver(action_text, patient_info["name"], patient_info["bed_number"])
                previous_button = detected_button

    return jsonify(result)

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global cap, active_features, detected_button, previous_button

    if cap is not None:
        cap.release()
        cap = None

    active_features.clear()
    detected_button = None
    previous_button = None

    return jsonify({"status": "success", "message": "Monitoring stopped"})

# Clean up resources when the app is shutting down
def cleanup():
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        cleanup()