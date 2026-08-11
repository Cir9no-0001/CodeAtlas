-- Find Total Time Spent by Each Employee
-- https://leetcode.com/problems/find-total-time-spent-by-each-employee
-- difficulty: easy
-- first_seen: 2026-08-11 15:11:35 EDT
-- runtime: 590ms

/*
Notes:

*/


select
    e.event_day as 'day',
    e.emp_id,
    (sum(e.out_time)-sum(e.in_time)) as 'total_time'
from Employees e
group by e.emp_id, e.event_day