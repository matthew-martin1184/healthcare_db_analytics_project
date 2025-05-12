-- =============================================================================
-- File: procedure_queries.sql
-- Author: Matthew Martin
-- Purpose: Summary-level provider/procedure queries
-- =============================================================================

-- =====================
-- PROCEDURE UTILIZATION
-- =====================

-- name: freq_of_proc
-- description: counts how many times each type of procedure (by name) appears in the medical_procedure table
SELECT
    procedure_name,
    COUNT(*) AS procedure_count
FROM
    medical_procedure
GROUP BY
    procedure_name
ORDER BY
    procedure_count DESC;

-- name: num_procs_per_appt
-- description: calculates how many procedures were performed during each appointment
SELECT
    appointment_id,
    COUNT(procedure_id) AS num_procedures
FROM
    medical_procedure
GROUP BY
    appointment_id
ORDER BY
    num_procedures DESC;

-- =====================
-- PROCEDURE PERFORMANCE
-- =====================

-- name: proc_performance_sum
-- description: lists each procedure type with total times performed and total billing amount generated
SELECT
    mp.procedure_name,
    COUNT(mp.procedure_id) AS procedure_count,
    SUM(b.amount) AS total_billed
FROM
    medical_procedure mp
JOIN
    appointment a ON mp.appointment_id = a.appointment_id
JOIN
    billing b ON a.patient_id = b.patient_id
GROUP BY
    mp.procedure_name
ORDER BY
    procedure_count DESC;
