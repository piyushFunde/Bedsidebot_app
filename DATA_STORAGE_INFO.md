# BedsideBot Data Storage Information

## 📊 **Where All Data Gets Stored**

### **🗄️ Database Storage (SQLite)**

#### **Database File Location:**
- **File**: `bedsidebot.db` (created automatically)
- **Location**: Same folder as `app.py`
- **Type**: SQLite database (portable, no setup required)

#### **Database Tables:**

### **1. Hospital Registration Data**
**Table**: `hospitals`
```sql
- hospital_name (Hospital name)
- hospital_id (Unique hospital ID)
- address (Full address)
- phone (Contact number)
- email (Email address)
- license_number (Hospital license)
- administrator_name (Admin name)
- total_beds (Total bed count)
- departments (Medical specialties - JSON)
- created_at (Registration timestamp)
```

### **2. Staff Registration Data**
**Table**: `staff`
```sql
- staff_id (Employee ID)
- full_name (Staff full name)
- role (nurse, doctor, admin, etc.)
- department (ICU, Emergency, etc.)
- phone (Contact number)
- email (Email address)
- license_number (Professional license)
- shift_schedule (Day/Night/Rotating)
- password_hash (Encrypted password)
- is_active (Active status)
- created_at (Registration timestamp)
```

### **3. Patient Registration Data**
**Table**: `patients`
```sql
- patient_id (Unique patient ID)
- full_name (Patient full name)
- date_of_birth (Birth date)
- gender (Male/Female/Other)
- blood_type (A+, B-, etc.)
- primary_condition (Medical condition)
- mobility_level (Bedridden, Mobile, etc.)
- medical_history (Medical background)
- attending_physician (Doctor name)
- room_number (Hospital room)
- bed_number (Bed assignment)
- department (ICU, Cardiology, etc.)
- care_level (Intensive, Moderate, etc.)
- assigned_nurse_id (Nurse ID)
- communication_methods (Voice, Gestures - JSON)
- communication_notes (Special instructions)
- admission_date (Hospital admission date)
- is_active (Active monitoring status)
```

### **4. Patient Requests/Inputs**
**Table**: `patient_requests`
```sql
- patient_id (Which patient made request)
- request_type (1=Nurse, 2=Water, 3=Food, 4=Bathroom, 5=Emergency)
- request_method (gesture, voice, manual)
- request_message (Description of request)
- timestamp (When request was made)
- response_time (When staff responded)
- responded_by (Staff member ID)
- response_notes (Staff notes)
- status (pending, acknowledged, completed)
- room_number (Patient room)
- bed_number (Patient bed)
- urgency_level (normal, high, critical)
```

### **5. Caregiver Registration Data**
**Table**: `caregivers`
```sql
- full_name (Caregiver name)
- relationship (Spouse, Parent, etc.)
- phone (Contact number)
- email (Email address)
- address (Home address)
- emergency_contact (Is emergency contact?)
- patient_ids (Associated patients - JSON)
- notification_methods (SMS, Email, etc. - JSON)
- notification_schedule (When to notify - JSON)
- created_at (Registration timestamp)
```

### **6. System Analytics**
**Table**: `system_analytics`
```sql
- date (Analytics date)
- total_patients (Patient count)
- total_requests (Request count)
- emergency_requests (Emergency count)
- nurse_requests (Nurse call count)
- water_requests (Water request count)
- food_requests (Food request count)
- bathroom_requests (Bathroom request count)
- avg_response_time (Average response time)
- requests_completed (Completed requests)
```

## 🔍 **How to View Stored Data**

### **Method 1: Through Application**
- **ICU Dashboard**: `/icu_dashboard` - View all patients
- **Analytics**: `/analytics` - View system statistics
- **Patient Details**: Click patient cards to see full info
- **Print Reports**: Generate reports with all patient data

### **Method 2: Direct Database Access**
```bash
# Install SQLite browser (optional)
# Download: https://sqlitebrowser.org/

# Or use command line
sqlite3 bedsidebot.db
.tables                    # Show all tables
SELECT * FROM patients;    # View all patients
SELECT * FROM patient_requests; # View all requests
```

### **Method 3: Test Routes**
- **All Patients**: `/test/patients` - List all registered patients
- **Database Status**: Check if data exists

## 💾 **Data Persistence**

### **Permanent Storage**
- ✅ **All form data** saved to SQLite database
- ✅ **Patient requests** stored with timestamps
- ✅ **Staff responses** tracked and logged
- ✅ **System analytics** calculated and stored
- ✅ **Data survives** server restarts

### **Temporary Storage**
- **Registration flow**: Stored in memory during registration process
- **Latest requests**: Cached for real-time notifications
- **Active sessions**: Current monitoring sessions

## 🔒 **Data Security**

### **Protection Measures**
- **Input Sanitization**: All form inputs cleaned
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: HTML content escaped
- **Rate Limiting**: Prevents spam requests
- **Validation**: Required fields enforced

### **Data Backup**
- **Database File**: `bedsidebot.db` can be copied for backup
- **Cloud Deployment**: Railway automatically backs up data
- **Export Options**: Print reports for physical records

## 📱 **Real-Time Data Flow**

### **Patient Makes Request**
1. **Patient Interface** → Button click/voice command
2. **Server** → Saves to `patient_requests` table
3. **ICU Dashboard** → Shows real-time notification
4. **Staff Response** → Updates request status in database

### **Registration Process**
1. **Form Submission** → Validates required fields
2. **Server Processing** → Sanitizes and validates data
3. **Database Storage** → Saves to appropriate table
4. **Confirmation** → Success message to user

## 🚨 **Data Troubleshooting**

### **If Data Not Saving**
- Check database file exists: `bedsidebot.db`
- Verify all required fields filled
- Check server logs for errors
- Ensure proper form submission

### **If Patients Not Showing**
- Check `/test/patients` to see if patients exist
- Verify patient registration completed successfully
- Check `is_active` status in database

### **If Requests Not Logging**
- Verify patient exists in database
- Check patient interface is working
- Monitor server console for errors
- Check `patient_requests` table directly

---

**All your data is safely stored in the SQLite database and can be accessed through the application interface or directly through database tools.**