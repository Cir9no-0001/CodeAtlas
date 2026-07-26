-- Patients With a Condition
-- https://leetcode.com/problems/patients-with-a-condition
-- difficulty: easy
-- first_seen: 2026-07-25 21:19:42 EDT
-- runtime: 488ms
-- Notes:
--


select 
    p.patient_id,
    p.patient_name,
    p.conditions
from Patients p
where p.conditions like '% DIAB1%' or p.conditions like 'DIAB1%'