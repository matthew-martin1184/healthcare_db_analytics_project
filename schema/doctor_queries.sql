-- =============================================================================
-- File: doctor_queries.sql
-- Author: Matthew Martin
-- Purpose: Summary-level doctor-focused queries
-- =============================================================================

-- =============================================
--  DOCTOR WORKLOAD, SCHEDULING, AND UTILIZATION
-- =============================================

-- name: appts_per_doctor
-- description: returns a count appointments per doctor, including doctors with zero appointments, sorted by highest volume
SELECT
    d.doctor_id,
    d.doctor_name,
    COUNT(a.appointment_id) AS num_appointments
FROM
    doctor d
LEFT JOIN
    appointment a ON d.doctor_id = a.doctor_id
GROUP BY
    d.doctor_id, d.doctor_name
ORDER BY
    num_appointments DESC;

-- name: doctor_utilize_rate
-- description: compares each doctor's monthly appointment count to capacity (100 per month) and calculates utilization percentage
SELECT
    d.doctor_id,
    d.doctor_name,
    TO_CHAR(a.appointment_date, 'YYYY-MM') AS month,
    COUNT(a.appointment_id) AS appointments_in_month,
    100 AS monthly_capacity,
    ROUND((COUNT(a.appointment_id) / 100) * 100, 2) AS utilization_pct
FROM
    doctor d
LEFT JOIN
    appointment a ON d.doctor_id = a.doctor_id
GROUP BY
    d.doctor_id,
    d.doctor_name,
    TO_CHAR(a.appointment_date, 'YYYY-MM')
ORDER BY
    d.doctor_name,
    month;

-- ===========================
--  DOCTOR–PROCEDURE INSIGHTS
-- ===========================

-- name: doctor_proc_freq
-- description: calculates how many times each procedure was performed by each doctor, sorted by the most common combinations
SELECT
    doctor_id,
    doctor_name,
    procedure_name,
    COUNT(*) AS procedure_count
FROM (
    SELECT
        d.doctor_id,
        d.doctor_name,
        mp.procedure_name
    FROM
        doctor d
    JOIN
        appointment a ON d.doctor_id = a.doctor_id
    JOIN
        medical_procedure mp ON a.appointment_id = mp.appointment_id
)
GROUP BY
    doctor_id, doctor_name, procedure_name
ORDER BY
    procedure_count DESC;

-- name: avg_num_procs_per_appt_by_doctor
-- description: calculates how many procedures, on average, each doctor performs per appointment, including appointments with zero procedures
SELECT
    d.doctor_id,
    d.doctor_name,
    ROUND(COUNT(mp.procedure_id) * 1.0 / COUNT(DISTINCT a.appointment_id), 2) AS avg_procedures_per_appt
FROM
    doctor d
JOIN
    appointment a ON d.doctor_id = a.doctor_id
LEFT JOIN
    medical_procedure mp ON a.appointment_id = mp.appointment_id
GROUP BY
    d.doctor_id, d.doctor_name
ORDER BY
    avg_procedures_per_appt DESC;

-- name: doctors_by_range_of_procs
-- description: Identifies doctors who have performed the most diverse set of procedures, based on the number of distinct procedure names
SELECT
    d.doctor_id,
    d.doctor_name,
    COUNT(DISTINCT mp.procedure_name) AS unique_procedures
FROM
    doctor d
JOIN
    appointment a ON d.doctor_id = a.doctor_id
JOIN
    medical_procedure mp ON a.appointment_id = mp.appointment_id
GROUP BY
    d.doctor_id, d.doctor_name
ORDER BY
    unique_procedures DESC;

-- ================================
--  DOCTOR SPECIALIZATION BREAKDOWN
-- ================================

-- name: specialty_resource_allocation
-- despcription: total appointments and revenue per specialty, plus derived appointments-per-doctor and revenue-per-doctor
SELECT
    d.specialization,
    COUNT(DISTINCT d.doctor_id) AS num_doctors,
    COUNT(a.appointment_id) AS total_appointments,
    ROUND(COUNT(a.appointment_id) * 1.0 / COUNT(DISTINCT d.doctor_id), 2) AS appts_per_doctor,
    COALESCE(SUM(b.amount), 0) AS total_revenue,
    ROUND(COALESCE(SUM(b.amount), 0) * 1.0 / COUNT(DISTINCT d.doctor_id), 2) AS revenue_per_doctor
FROM
    doctor d
LEFT JOIN
    appointment a ON d.doctor_id = a.doctor_id
LEFT JOIN
    billing b ON a.patient_id = b.patient_id
GROUP BY
    d.specialization
ORDER BY
    appts_per_doctor DESC;

-- name: num_doctors_per_spec
-- description: counts how many doctors belong to each specialization
SELECT
    specialization,
    COUNT(*) AS num_doctors
FROM
    doctor
GROUP BY
    specialization
ORDER BY
    num_doctors DESC;

-- name: ttl_appts_per_spec
-- description: counts the total number of appointments handled by each specialization, reflecting overall workload or patient volume by specialty
SELECT
    d.specialization,
    COUNT(a.appointment_id) AS total_appointments
FROM
    doctor d
JOIN
    appointment a ON d.doctor_id = a.doctor_id
GROUP BY
    d.specialization
ORDER BY
    total_appointments DESC;

-- ===================
--  DOCTOR PERFORMANCE
-- ===================

-- name: doctor_performance_dash
-- description: aggregated view per doctor showing total appointments, procedures performed, and total billing amount
SELECT
    d.doctor_id,
    d.doctor_name,
    NVL(ac.appt_count, 0)    AS total_appointments,
    NVL(pc.proc_count, 0)    AS total_procedures,
    NVL(bt.total_billed, 0)  AS total_billing
FROM
    doctor d
LEFT JOIN (
    SELECT a1.doctor_id, COUNT(a1.appointment_id) AS appt_count
    FROM appointment a1
    GROUP BY a1.doctor_id
) ac ON d.doctor_id = ac.doctor_id
LEFT JOIN (
    SELECT a2.doctor_id, COUNT(mp.procedure_id) AS proc_count
    FROM appointment a2
    JOIN medical_procedure mp ON a2.appointment_id = mp.appointment_id
    GROUP BY a2.doctor_id
) pc ON d.doctor_id = pc.doctor_id
LEFT JOIN (
    SELECT a3.doctor_id, SUM(b.amount) AS total_billed
    FROM appointment a3
    JOIN billing b ON a3.patient_id = b.patient_id
    GROUP BY a3.doctor_id
) bt ON d.doctor_id = bt.doctor_id
ORDER BY
    total_appointments DESC;
