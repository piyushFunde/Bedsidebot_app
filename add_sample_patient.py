#!/usr/bin/env python3
"""
Sample Patient Data Script
Adds a sample patient to the database for testing the ICU dashboard functionality
"""

import sys
import os
from datetime import date, datetime
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db, Patient

def add_sample_patient():
    """Add a sample patient to the database"""
    
    with app.app_context():
        # Check if sample patient already exists
        existing_patient = Patient.query.filter_by(patient_id='P001').first()
        if existing_patient:
            print("Sample patient P001 already exists!")
            return
        
        # Create sample patient
        sample_patient = Patient(
            patient_id='P001',
            full_name='John Smith',
            date_of_birth=date(1975, 3, 15),
            gender='male',
            blood_type='A+',
            phone='555-0123',
            emergency_contact='Jane Smith (Wife)',
            emergency_phone='555-0124',
            primary_condition='Post-surgical recovery',
            mobility_level='limited-mobility',
            medical_history='Appendectomy performed 2 days ago. History of hypertension, managed with medication.',
            allergies='Penicillin, Shellfish',
            current_medications='Lisinopril 10mg daily, Acetaminophen as needed for pain',
            attending_physician='Dr. Sarah Johnson',
            room_number='101',
            bed_number='A',
            department='icu',
            care_level='intensive',
            assigned_nurse_id='N001',
            communication_methods=json.dumps(['voice', 'hand-gestures', 'facial-expressions']),
            communication_notes='Patient prefers voice commands but can use gestures when tired. Speaks English fluently.',
            admission_date=date.today(),
            is_active=True,
            monitoring_status='active'
        )
        
        try:
            db.session.add(sample_patient)
            db.session.commit()
            print("✅ Sample patient 'John Smith' (P001) added successfully!")
            print("   - Room: 101, Bed: A")
            print("   - Department: ICU")
            print("   - Condition: Post-surgical recovery")
            print("   - You can now view this patient in the ICU Dashboard")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding sample patient: {e}")

def add_more_sample_patients():
    """Add additional sample patients for testing"""
    
    with app.app_context():
        patients_data = [
            {
                'patient_id': 'P002',
                'full_name': 'Maria Garcia',
                'date_of_birth': date(1982, 7, 22),
                'gender': 'female',
                'blood_type': 'O-',
                'primary_condition': 'Cardiac monitoring',
                'room_number': '102',
                'bed_number': 'B',
                'department': 'cardiology',
                'care_level': 'moderate',
                'medical_history': 'Recent myocardial infarction. Stable condition.',
                'communication_methods': json.dumps(['voice', 'eye-tracking']),
                'communication_notes': 'Patient speaks Spanish primarily, some English.'
            },
            {
                'patient_id': 'P003',
                'full_name': 'Robert Johnson',
                'date_of_birth': date(1968, 11, 8),
                'gender': 'male',
                'blood_type': 'B+',
                'primary_condition': 'Stroke recovery',
                'room_number': '103',
                'bed_number': 'A',
                'department': 'neurology',
                'care_level': 'intensive',
                'medical_history': 'Ischemic stroke 5 days ago. Limited speech ability.',
                'communication_methods': json.dumps(['eye-tracking', 'facial-expressions']),
                'communication_notes': 'Patient has difficulty speaking. Responds well to yes/no questions with eye movements.'
            }
        ]
        
        for patient_data in patients_data:
            existing = Patient.query.filter_by(patient_id=patient_data['patient_id']).first()
            if existing:
                print(f"Patient {patient_data['patient_id']} already exists, skipping...")
                continue
            
            patient = Patient(
                patient_id=patient_data['patient_id'],
                full_name=patient_data['full_name'],
                date_of_birth=patient_data['date_of_birth'],
                gender=patient_data['gender'],
                blood_type=patient_data['blood_type'],
                primary_condition=patient_data['primary_condition'],
                room_number=patient_data['room_number'],
                bed_number=patient_data['bed_number'],
                department=patient_data['department'],
                care_level=patient_data['care_level'],
                medical_history=patient_data['medical_history'],
                communication_methods=patient_data['communication_methods'],
                communication_notes=patient_data['communication_notes'],
                admission_date=date.today(),
                is_active=True,
                monitoring_status='active'
            )
            
            try:
                db.session.add(patient)
                db.session.commit()
                print(f"✅ Added patient: {patient_data['full_name']} ({patient_data['patient_id']})")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error adding patient {patient_data['patient_id']}: {e}")

if __name__ == '__main__':
    print("🏥 Adding sample patients to BedsideBot database...")
    print("=" * 50)
    
    add_sample_patient()
    add_more_sample_patients()
    
    print("\n" + "=" * 50)
    print("✅ Sample patients setup complete!")
    print("\n📋 To test the functionality:")
    print("1. Start the BedsideBot application")
    print("2. Go to /icu_dashboard")
    print("3. Click on any patient card to view details")
    print("4. Click 'Print Report' to generate a comprehensive report")
    print("5. The report will open in a new window with print-ready formatting")