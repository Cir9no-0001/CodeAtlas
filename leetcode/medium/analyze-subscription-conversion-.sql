-- Analyze Subscription Conversion 
-- https://leetcode.com/problems/analyze-subscription-conversion
-- difficulty: medium
-- first_seen: 2026-08-01 16:13:07 EDT
-- runtime: 660ms

/*
Notes:
Hint: almost pure logic/math question; make sure that the average part includes a distinct before the case statement to count only the distinct days the user has used the plan. Filter out the people who didn't upgrade from the free plan by only keeping those with activity durations in both the free and paid plans. [TC: O(NlogN), 4 passes]
*/

select
    u.user_id,
    round(sum(case when u.activity_type = 'free_trial' then u.activity_duration else 0 end)/count(distinct case when u.activity_type = 'free_trial' then u.activity_date end), 2) as 'trial_avg_duration',
    round(sum(case when u.activity_type = 'paid' then u.activity_duration else 0 end)/count(distinct case when u.activity_type = 'paid' then u.activity_date end), 2) as 'paid_avg_duration'
from UserActivity u
group by u.user_id
having trial_avg_duration!= 0 and paid_avg_duration != 0
order by u.user_id asc