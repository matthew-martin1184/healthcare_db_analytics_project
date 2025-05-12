-- =============================================================================
-- File: patient_queries.sql
-- Author: Matthew Martin
-- Purpose: Summary-level doctor-focused queries
-- =============================================================================

-- ==================================
--  PATIENT ENGAGEMENT & UTILIZATION
-- ==================================

-- name: ttl_appts_per_patient
-- description: lists each patient along with their number of recorded appointments, sorted from most to least
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    COUNT(a.appointment_id) AS num_appointments
FROM 
    patient p
LEFT JOIN 
    appointment a ON p.patient_id = a.patient_id
GROUP BY 
    p.patient_id, p.first_name, p.last_name
ORDER BY 
    num_appointments DESC;

-- name: avg_num_proc_per_appt_per_patient
-- description: calculates, for each patient, the average number of medical procedures per appointment
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    ROUND(COUNT(mp.procedure_id) * 1.0 / COUNT(DISTINCT a.appointment_id), 2) AS avg_procedures_per_appointment
FROM
    patient p
JOIN
    appointment a ON p.patient_id = a.patient_id
LEFT JOIN
    medical_procedure mp ON a.appointment_id = mp.appointment_id
GROUP BY
    p.patient_id, p.first_name, p.last_name
ORDER BY
    avg_procedures_per_appointment DESC;

-- name: patients_with_multiple_doctors
-- description: Identifies patients who have seen more than one doctor by counting distinct doctor IDs per patient   
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    COUNT(DISTINCT a.doctor_id) AS num_doctors_seen
FROM
    patient p
JOIN
    appointment a ON p.patient_id = a.patient_id
GROUP BY
    p.patient_id, p.first_name, p.last_name
HAVING
    COUNT(DISTINCT a.doctor_id) > 1
ORDER BY
    num_doctors_seen DESC;

-- ============================
--  RETURNING VS. NEW PATIENTS
-- ============================

-- name: new_vs_returning
-- description: classifies patients as "New" or "Returning" based on number of appointments
SELECT
    CASE
        WHEN COUNT(a.appointment_id) = 1 THEN 'New'
        ELSE 'Returning'
    END AS patient_status,
    COUNT(*) AS num_patients
FROM
    patient p
JOIN
    appointment a ON p.patient_id = a.patient_id
GROUP BY
    p.patient_id
ORDER BY
    patient_status;

-- ===============
--  PATIENT DEMAND
-- ===============

-- name: patient_demand
-- description: identifies patients with the highest appointment volume and procedure count
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(mp.procedure_id) AS total_procedures
FROM
    patient p
LEFT JOIN
    appointment a ON p.patient_id = a.patient_id
LEFT JOIN
    medical_procedure mp ON a.appointment_id = mp.appointment_id
GROUP BY
    p.patient_id,
    p.first_name,
    p.last_name
ORDER BY
    total_appointments DESC,
    total_procedures DESC;
