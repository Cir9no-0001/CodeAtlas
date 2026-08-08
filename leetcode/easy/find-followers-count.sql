-- Find Followers Count
-- https://leetcode.com/problems/find-followers-count
-- difficulty: easy
-- first_seen: 2026-08-08 16:09:35 EDT
-- runtime: 529ms

/*
Notes:

*/


select
    f.user_id,
    count(distinct f.follower_id) as 'followers_count'
from Followers f
group by f.user_id