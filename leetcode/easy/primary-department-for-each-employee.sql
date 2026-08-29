-- Primary Department for Each Employee
-- https://leetcode.com/problems/primary-department-for-each-employee
-- difficulty: easy
-- first_seen: 2026-08-29 03:06:58 EDT
-- runtime: 585ms

/*
Notes:

*/

select 
    e.employee_id, 
    coalesce(
        max(case when e.primary_flag = 'Y' then e.department_id end), 
        max(e.department_id)
    ) as 'department_id'
from Employee e
group by e.employee_id