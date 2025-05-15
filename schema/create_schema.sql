-- =============================================================================
-- File: create_schema
-- Author: Matthew Martin
-- Purpose: CREATE TABLE statements, constraints, and comments
-- =============================================================================

-- 🔹 Patients Table
CREATE TABLE patient (
    patient_id       NUMBER PRIMARY KEY,
    first_name       VARCHAR2(100),
    last_name        VARCHAR2(100),
    Email           VARCHAR2(150)
);

-- 🔹 Doctors Table
CREATE TABLE doctor (
    doctor_id        NUMBER PRIMARY KEY,
    doctor_name      VARCHAR2(100),
    specialization  VARCHAR2(100),
    doctor_contact   VARCHAR2(50)
);

-- 🔹 Appointments Table
CREATE TABLE appointment (
    appointment_id   NUMBER PRIMARY KEY,
    appointment_date      DATE,
    appointment_time      TIMESTAMP,
    patient_id       NUMBER,
    doctor_id        NUMBER,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id)  REFERENCES doctor(doctor_id)
);

-- 🔹 MedicalProcedure Table
CREATE TABLE medical_procedure (
    procedure_id    NUMBER PRIMARY KEY,
    procedure_name   VARCHAR2(100),
    appointment_id   NUMBER,
    FOREIGN KEY (appointment_id) REFERENCES appointment(appointment_id)
);

-- 🔹 Billing Table
CREATE TABLE billing (
    invoice_id       VARCHAR2(50) PRIMARY KEY,
    patient_id       NUMBER,
    items           VARCHAR2(255),
    amount      NUMBER(10,2),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
);

-- =============================================================================
-- Table, Column, and Key Comments
-- =============================================================================

-- patient Table

COMMENT ON TABLE patient IS 
    'Stores unique patient ID, first and last name, and email.';

-- doctor Table   

COMMENT ON TABLE doctor IS 
    'Stores heathcare provider name, medical specialization, and contact information.';

-- appointment Table    

COMMENT ON TABLE appointment IS 
    'Records scheduled appointments, linking patients to doctors.';

COMMENT ON COLUMN appointment.patient_id IS 
    'Foreign key to patient.patient_id';

COMMENT ON COLUMN appointment.doctor_id IS  
    'Foreign key to doctor.doctor_id';

-- medical_procedure Table    

COMMENT ON TABLE medical_procedure IS 
    'stores details about medical procedures associated with specific appointments.';

COMMENT ON COLUMN medical_procedure.appointment_id IS
    'Foreign key to appointment.appointment_id';   

-- billing Table    

COMMENT ON TABLE billing IS 
    'Maintains records of billing transactions, associating them with specific patients.';

COMMENT ON COLUMN billing.items IS
    'Description of items or services billed.';   

COMMENT ON COLUMN billing.amount IS
    'Amount charged for the billing transaction.';

COMMENT ON COLUMN billing.patient_id IS
    'Foreign key to patient.patient_id';

