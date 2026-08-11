-- The Number of Employees Which Report to Each Employee
-- https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee
-- difficulty: easy
-- first_seen: 2026-08-10 20:40:20 EDT
-- runtime: 615ms

/*
Notes:

*/


select
    e.reports_to as 'employee_id',
    em.name,
    count(e.employee_id) as 'reports_count',
    round(avg(e.age), 0) as 'average_age'
from Employees e
inner join Employees em
    on em.employee_id = e.reports_to
    where e.reports_to is not null
    
group by e.reports_to, em.name
order by e.reports_to