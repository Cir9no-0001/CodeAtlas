-- Patients With a Condition
-- https://leetcode.com/problems/patients-with-a-condition
-- difficulty: easy
-- first_seen: 2026-07-25 21:19:42 EDT
-- runtime: 488ms

/*
Notes:
Hint: make sure that DIAB1 is either the beginning of the first condition name or the
beginning of the condition name subsequently. [TC: O(n), 1 pass]
*/

select 
    p.patient_id,
    p.patient_name,
    p.conditions
from Patients p
where p.conditions like '% DIAB1%' or p.conditions like 'DIAB1%'