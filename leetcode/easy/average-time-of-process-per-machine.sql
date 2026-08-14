-- Average Time of Process per Machine
-- https://leetcode.com/problems/average-time-of-process-per-machine
-- difficulty: easy
-- first_seen: 2026-08-02 21:01:18 EDT
-- runtime: 269ms

/*
Notes:
Hint: literally a math question; think about how you can rearrange the original formula
to optimize it for SQL grouping. Group by the IDs, then split each group into its
corresponding activity type, then find the difference and divide by the distinct
processes. [O(NlogN), 1 pass]
*/

select 
    a.machine_id,
    round(
        (sum(case when a.activity_type = 'end' then a.timestamp else 0 end)-
        sum(case when a.activity_type = 'start' then a.timestamp else 0 end))
        /count(distinct a.process_id)
    , 3) as 'processing_time'
from Activity a
group by a.machine_id