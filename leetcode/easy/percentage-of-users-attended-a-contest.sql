-- Percentage of Users Attended a Contest
-- https://leetcode.com/problems/percentage-of-users-attended-a-contest
-- difficulty: easy
-- first_seen: 2026-07-27 23:56:04 EDT
-- runtime: 982ms
-- Notes:
-- Hint: math problem, group by contest_id, then count, then divide by the total number of users. [TC: O(N+MlogM), 2 passes]


select 
    r.contest_id, 
    round(count(distinct r.user_id) * 100 /(select count(user_id) from Users) ,2) as 'percentage'
from Register r
group by r.contest_id
order by percentage desc, r.contest_id asc