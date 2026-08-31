-- Calculate Special Bonus
-- https://leetcode.com/problems/calculate-special-bonus
-- difficulty: easy
-- first_seen: 2026-08-31 12:17:09 EDT
-- runtime: 614ms

/*
Notes:

*/

select
    e.employee_id,
    case when e.employee_id % 2 = 1 and e.name not like 'M%' then e.salary else 0 end as 'bonus'
from Employees e
order by e.employee_id