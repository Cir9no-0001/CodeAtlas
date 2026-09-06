-- Number of Unique Subjects Taught by Each Teacher
-- https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher
-- difficulty: easy
-- first_seen: 2026-09-06 12:46:05 EDT
-- runtime: 691ms

/*
Notes:

*/

select
    t.teacher_id,
    count(distinct t.subject_id) as 'cnt'
from Teacher t
group by t.teacher_id