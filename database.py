from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

# Hospital Registration Table
class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(200), nullable=False)
    hospital_id = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    license_number = db.Column(db.String(100))
    administrator_name = db.Column(db.String(100))
    total_beds = db.Column(db.Integer)
    departments = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_name': self.hospital_name,
            'hospital_id': self.hospital_id,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'license_number': self.license_number,
            'administrator_name': self.administrator_name,
            'total_beds': self.total_beds,
            'departments': json.loads(self.departments) if self.departments else [],
            'created_at': self.created_at.isoformat()
        }

# Staff Registration Table
class Staff(db.Model):
    __tablename__ = 'staff'
    
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # nurse, doctor, admin
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    license_number = db.Column(db.String(100))
    shift_schedule = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'full_name': self.full_name,
            'role': self.role,
            'department': self.department,
            'phone': self.phone,
            'email': self.email,
            'license_number': self.license_number,
            'shift_schedule': self.shift_schedule,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

# Patient Registration Table
class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    blood_type = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    
    # Medical Information
    primary_condition = db.Column(db.String(200), nullable=False)
    secondary_conditions = db.Column(db.Text)  # JSON string
    mobility_level = db.Column(db.String(50))
    medical_history = db.Column(db.Text)
    allergies = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    attending_physician = db.Column(db.String(100))
    
    # Hospital Assignment
    room_number = db.Column(db.String(20), nullable=False)
    bed_number = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    care_level = db.Column(db.String(50), nullable=False)
    assigned_nurse_id = db.Column(db.String(50))
    
    # Communication Preferences
    communication_methods = db.Column(db.Text)  # JSON string
    communication_notes = db.Column(db.Text)
    
    # Status
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    monitoring_status = db.Column(db.String(50), default='inactive')  # active, inactive, paused
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'blood_type': self.blood_type,
            'phone': self.phone,
            'emergency_contact': self.emergency_contact,
            'emergency_phone': self.emergency_phone,
            'primary_condition': self.primary_condition,
            'secondary_conditions': json.loads(self.secondary_conditions) if self.secondary_conditions else [],
            'mobility_level': self.mobility_level,
            'medical_history': self.medical_history,
            'allergies': self.allergies,
            'current_medications': self.current_medications,
            'attending_physician': self.attending_physician,
            'room_number': self.room_number,
            'bed_number': self.bed_number,
            'department': self.department,
            'care_level': self.care_level,
            'assigned_nurse_id': self.assigned_nurse_id,
            'communication_methods': json.loads(self.communication_methods) if self.communication_methods else [],
            'communication_notes': self.communication_notes,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
            'is_active': self.is_active,
            'monitoring_status': self.monitoring_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Patient Requests/Interactions Table
class PatientRequest(db.Model):
    __tablename__ = 'patient_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), nullable=False)
    request_type = db.Column(db.Integer, nullable=False)  # 1-5 (nurse, water, food, bathroom, emergency)
    request_method = db.Column(db.String(20), nullable=False)  # gesture, voice, manual
    request_message = db.Column(db.String(200))
    
    # Timing and Response
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response_time = db.Column(db.DateTime)
    responded_by = db.Column(db.String(50))  # staff_id
    response_notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, acknowledged, completed, cancelled
    
    # Context Information
    room_number = db.Column(db.String(20))
    bed_number = db.Column(db.String(20))
    shift_time = db.Column(db.String(20))  # morning, afternoon, night
    urgency_level = db.Column(db.String(20), default='normal')  # low, normal, high, critical
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'request_type': self.request_type,
            'request_method': self.request_method,
            'request_message': self.request_message,
            'timestamp': self.timestamp.isoformat(),
            'response_time': self.response_time.isoformat() if self.response_time else None,
            'responded_by': self.responded_by,
            'response_notes': self.response_notes,
            'status': self.status,
            'room_number': self.room_number,
            'bed_number': self.bed_number,
            'shift_time': self.shift_time,
            'urgency_level': self.urgency_level
        }

# Monitoring Sessions Table
class MonitoringSession(db.Model):
    __tablename__ = 'monitoring_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), nullable=False)
    session_start = db.Column(db.DateTime, default=datetime.utcnow)
    session_end = db.Column(db.DateTime)
    monitoring_nurse_id = db.Column(db.String(50))
    
    # Session Statistics
    total_requests = db.Column(db.Integer, default=0)
    gesture_requests = db.Column(db.Integer, default=0)
    voice_requests = db.Column(db.Integer, default=0)
    emergency_requests = db.Column(db.Integer, default=0)
    
    # Features Used
    features_enabled = db.Column(db.Text)  # JSON string
    camera_status = db.Column(db.String(20), default='inactive')
    voice_status = db.Column(db.String(20), default='inactive')
    
    session_notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'session_start': self.session_start.isoformat(),
            'session_end': self.session_end.isoformat() if self.session_end else None,
            'monitoring_nurse_id': self.monitoring_nurse_id,
            'total_requests': self.total_requests,
            'gesture_requests': self.gesture_requests,
            'voice_requests': self.voice_requests,
            'emergency_requests': self.emergency_requests,
            'features_enabled': json.loads(self.features_enabled) if self.features_enabled else [],
            'camera_status': self.camera_status,
            'voice_status': self.voice_status,
            'session_notes': self.session_notes
        }

# Caregiver Registration Table
class Caregiver(db.Model):
    __tablename__ = 'caregivers'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50))  # family, friend, guardian
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.Boolean, default=False)
    
    # Associated Patients
    patient_ids = db.Column(db.Text)  # JSON string of patient IDs
    
    # Notification Preferences
    notification_methods = db.Column(db.Text)  # JSON string
    notification_schedule = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'relationship': self.relationship,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'patient_ids': json.loads(self.patient_ids) if self.patient_ids else [],
            'notification_methods': json.loads(self.notification_methods) if self.notification_methods else [],
            'notification_schedule': json.loads(self.notification_schedule) if self.notification_schedule else {},
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

# System Analytics Table
class SystemAnalytics(db.Model):
    __tablename__ = 'system_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow().date())
    
    # Daily Statistics
    total_patients = db.Column(db.Integer, default=0)
    active_monitoring_sessions = db.Column(db.Integer, default=0)
    total_requests = db.Column(db.Integer, default=0)
    emergency_requests = db.Column(db.Integer, default=0)
    
    # Request Type Breakdown
    nurse_requests = db.Column(db.Integer, default=0)
    water_requests = db.Column(db.Integer, default=0)
    food_requests = db.Column(db.Integer, default=0)
    bathroom_requests = db.Column(db.Integer, default=0)
    
    # Response Metrics
    avg_response_time = db.Column(db.Float, default=0.0)  # in minutes
    requests_completed = db.Column(db.Integer, default=0)
    requests_pending = db.Column(db.Integer, default=0)
    
    # System Usage
    gesture_recognition_usage = db.Column(db.Integer, default=0)
    voice_recognition_usage = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'total_patients': self.total_patients,
            'active_monitoring_sessions': self.active_monitoring_sessions,
            'total_requests': self.total_requests,
            'emergency_requests': self.emergency_requests,
            'nurse_requests': self.nurse_requests,
            'water_requests': self.water_requests,
            'food_requests': self.food_requests,
            'bathroom_requests': self.bathroom_requests,
            'avg_response_time': self.avg_response_time,
            'requests_completed': self.requests_completed,
            'requests_pending': self.requests_pending,
            'gesture_recognition_usage': self.gesture_recognition_usage,
            'voice_recognition_usage': self.voice_recognition_usage,
            'created_at': self.created_at.isoformat()
        }

def init_database(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user if not exists
        admin_staff = Staff.query.filter_by(staff_id='ADMIN001').first()
        if not admin_staff:
            from security import security
            admin_staff = Staff(
                staff_id='ADMIN001',
                full_name='System Administrator',
                role='admin',
                department='IT',
                email='admin@bedsidebot.com',
                password_hash=security.hash_password('admin123'),
                is_active=True
            )
            db.session.add(admin_staff)
            db.session.commit()
            print("[INFO] Default admin user created: ADMIN001 / admin123")
        
        print("[INFO] Database initialized successfully")

def get_patient_request_patterns(patient_id, days=7):
    """Analyze patient request patterns for insights"""
    from datetime import timedelta
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    requests = PatientRequest.query.filter(
        PatientRequest.patient_id == patient_id,
        PatientRequest.timestamp >= start_date
    ).all()
    
    patterns = {
        'total_requests': len(requests),
        'request_types': {},
        'hourly_patterns': {},
        'method_preferences': {},
        'response_times': []
    }
    
    for request in requests:
        # Request type analysis
        req_type = request.request_type
        if req_type not in patterns['request_types']:
            patterns['request_types'][req_type] = 0
        patterns['request_types'][req_type] += 1
        
        # Hourly pattern analysis
        hour = request.timestamp.hour
        if hour not in patterns['hourly_patterns']:
            patterns['hourly_patterns'][hour] = 0
        patterns['hourly_patterns'][hour] += 1
        
        # Method preference analysis
        method = request.request_method
        if method not in patterns['method_preferences']:
            patterns['method_preferences'][method] = 0
        patterns['method_preferences'][method] += 1
        
        # Response time analysis
        if request.response_time:
            response_time = (request.response_time - request.timestamp).total_seconds() / 60
            patterns['response_times'].append(response_time)
    
    return patterns