"""
Auto-setup script for BedsideBot with demo data
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def register_demo_data():
    """Register demo hospital, staff, patient, and caregiver"""
    
    # 1. Register Hospital
    hospital_data = {
        "hospitalName": "Demo General Hospital",
        "hospitalId": "DGH001",
        "fullAddress": "123 Healthcare Street",
        "city": "Mumbai",
        "state": "Maharashtra", 
        "zipCode": "400001",
        "primaryPhone": "+912212345678",
        "email": "admin@demohospital.com",
        "adminName": "Dr. Admin",
        "licenseNumber": "MH001234",
        "totalBeds": "100",
        "icuBeds": "20"
    }
    
    print("Registering hospital...")
    response = requests.post(f"{BASE_URL}/api/register/hospital", json=hospital_data)
    print(f"Hospital: {response.json()}")
    
    # 2. Register Staff
    staff_data = {
        "fullName": "Nurse Sarah",
        "employeeId": "NS001",
        "role": "Registered Nurse",
        "department": "General Ward",
        "shift": "Day Shift",
        "phoneNumber": "+919876543210",
        "email": "sarah@demohospital.com",
        "experience": "5 years",
        "startDate": "2024-01-01",
        "employmentStatus": "Full-time",
        "accessLevel": "Standard",
        "notifications": True
    }
    
    print("Registering staff...")
    response = requests.post(f"{BASE_URL}/api/register/staff", json=staff_data)
    print(f"Staff: {response.json()}")
    
    # 3. Register Patient
    patient_data = {
        "fullName": "John Doe",
        "patientId": "P001",
        "dateOfBirth": "1980-01-15",
        "gender": "Male",
        "bloodType": "O+",
        "primaryCondition": "Post-surgery recovery",
        "mobilityLevel": "Limited",
        "medicalHistory": "Appendectomy",
        "attendingPhysician": "Dr. Smith",
        "roomNumber": "101",
        "bedNumber": "A",
        "department": "General Ward",
        "careLevel": "Standard",
        "assignedNurse": "NS001",
        "communicationMethods": ["gesture", "voice"],
        "communicationNotes": "Prefers gesture communication",
        "admissionDate": "2024-01-10"
    }
    
    print("Registering patient...")
    response = requests.post(f"{BASE_URL}/api/register/patient", json=patient_data)
    print(f"Patient: {response.json()}")
    
    # 4. Register Caregiver (Your details)
    caregiver_data = {
        "fullName": "Rahul Pharande",
        "caregiverId": "CG001",
        "relationship": "Family Member",
        "primaryPhone": "+919604226339",
        "email": "rahulspharande28@gmail.com",
        "accessLevel": "Full",
        "notifications": True,
        "contactMethod": "both",
        "decisionMaking": "Authorized",
        "availability": "24/7"
    }
    
    print("Registering caregiver...")
    response = requests.post(f"{BASE_URL}/api/register/caregiver", json=caregiver_data)
    print(f"Caregiver: {response.json()}")
    
    print("\n✅ Demo data setup complete!")
    print(f"🌐 Access the system at: {BASE_URL}")
    print(f"🧪 Test notifications at: {BASE_URL}/test_notifications")

if __name__ == "__main__":
    print("Setting up BedsideBot with demo data...")
    print("Make sure the server is running first!")
    
    try:
        # Wait a moment for server to be ready
        time.sleep(2)
        register_demo_data()
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("Make sure the server is running: python app.py")