-- Rising Temperature
-- https://leetcode.com/problems/rising-temperature
-- difficulty: easy
-- first_seen: 2026-07-05 20:40:05 EDT
-- runtime: 515
/*
Notes:

*/

Select w.id as Id
from Weather w
inner join Weather q
on DATEDIFF(w.recordDate, q.recordDate) = 1
where w.temperature>q.temperature;
