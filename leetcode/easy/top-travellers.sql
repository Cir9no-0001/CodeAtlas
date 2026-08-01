-- Top Travellers
-- https://leetcode.com/problems/top-travellers
-- difficulty: easy
-- first_seen: 2026-07-28 20:55:59 EDT
-- runtime: 978ms

/*
Notes:
Hint: users can exist without being on the rides table, so make sure null values default to 0; the same thing should be considered when joining. [TC: O(U+RlogU), 1 pass]
*/


select 
    u.name,
    ifnull(sum(r.distance), 0) as 'travelled_distance'
from Users u
left join Rides r
on r.user_id=u.id
group by r.user_id
order by travelled_distance desc, u.name asc