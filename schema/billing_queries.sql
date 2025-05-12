-- =============================================================================
-- File: billing_queries.sql
-- Author: Matthew Martin
-- Purpose: Summary-level billing-focused queries
-- =============================================================================

-- ==================
--  BILLING BY DOCTOR
-- ==================

-- name: ttl_billing_by_doctor
-- description: calculates the total billing amount indirectly attributed to each doctor via the patients they saw
SELECT
    d.doctor_id,
    d.doctor_name,
    SUM(b.amount) AS total_billed
FROM
    doctor d
JOIN
    appointment a ON d.doctor_id = a.doctor_id
JOIN
    billing b ON a.patient_id = b.patient_id
GROUP BY
    d.doctor_id, d.doctor_name
ORDER BY
    total_billed DESC;

-- name: avg_billed_amt_per_appt_by_doctor
-- description: calculates the average billed amount per appointment for each doctor by dividing total billed by the number of unique appointments
SELECT
    d.doctor_id,
    d.doctor_name,
    ROUND(SUM(b.amount) * 1.0 / COUNT(DISTINCT a.appointment_id), 2) AS avg_billed_per_appt
FROM
    doctor d
JOIN
    appointment a ON d.doctor_id = a.doctor_id
JOIN
    billing b ON a.patient_id = b.patient_id
GROUP BY
    d.doctor_id, d.doctor_name
ORDER BY
    avg_billed_per_appt DESC; 

-- name: proc_billing_summary_per_doctor
-- description: summary of procedure volume and average billing amount per procedure type by doctor
SELECT
    d.doctor_name,
    mp.procedure_name,
    COUNT(mp.procedure_id) AS procedure_count,
    ROUND(AVG(b.amount), 2) AS avg_billed_amount
FROM
    doctor d
JOIN
    appointment a ON d.doctor_id = a.doctor_id
JOIN
    medical_procedure mp ON a.appointment_id = mp.appointment_id
JOIN
    billing b ON a.patient_id = b.patient_id
GROUP BY
    d.doctor_name, mp.procedure_name
ORDER BY
    procedure_count DESC;    

-- ===================
--  BILLING BY PATIENT
-- ===================    

-- name: ttl_billing_per_patient
-- description: returns each patient’s total billing amount, sorted from highest to lowest
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    COALESCE(SUM(b.amount), 0) AS total_billed
FROM
    patient p
LEFT JOIN
    billing b ON p.patient_id = b.patient_id
GROUP BY
    p.patient_id, p.first_name, p.last_name
ORDER BY
    total_billed DESC;

-- ===============================
--  APPOINTMENT AND BILLING TRENDS
-- ===============================

-- name: avg_billing_by_hour
-- description: average billing amount for appointments during each hour of the day
SELECT
    TO_CHAR(appointment_time, 'HH24') AS hour_of_day,
    ROUND(AVG(b.amount), 2) AS avg_billed
FROM
    appointment a
JOIN
    billing b ON a.patient_id = b.patient_id
GROUP BY
    TO_CHAR(appointment_time, 'HH24')
ORDER BY
    hour_of_day;    

-- name: monthly_proc_and_billing_summary
-- description: monthly summary of the number of procedures performed and the total billing amount    
SELECT
    TO_CHAR(a.appointment_date, 'YYYY-MM') AS month,
    COUNT(mp.procedure_id) AS procedure_count,
    SUM(b.amount) AS total_billed
FROM
    appointment a
JOIN
    medical_procedure mp ON a.appointment_id = mp.appointment_id
JOIN
    billing b ON a.patient_id = b.patient_id
GROUP BY
    TO_CHAR(a.appointment_date, 'YYYY-MM')
ORDER BY
    month;

-- name: peak_hour_day
-- description: total number of appointments grouped by hour of day and day of week to identify peak times
SELECT
    TO_CHAR(a.appointment_time, 'DY') AS day_of_week,
    TO_CHAR(a.appointment_time, 'HH24') AS hour_of_day,
    COUNT(a.appointment_id) AS total_appointments
FROM
    appointment a
GROUP BY
    TO_CHAR(a.appointment_time, 'DY'),
    TO_CHAR(a.appointment_time, 'HH24')
ORDER BY
    total_appointments DESC;


       