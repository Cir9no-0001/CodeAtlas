-- Find Students Who Improved
-- https://leetcode.com/problems/find-students-who-improved
-- difficulty: medium
-- first_seen: 2026-07-31 09:22:35 EDT
-- runtime: 342ms
-- Notes:
--


with valid as (
    select 
        *, 
        rank() over (partition by s.student_id, s.subject order by exam_date asc) as 'first_rank',
        rank() over (partition by s.student_id, s.subject order by exam_date desc) as 'last_rank'
    from Scores s
)

select v.student_id, v.subject, v.score as 'first_score', va.score as 'latest_score'
from valid v
join valid va
    on (v.student_id, v.subject) = (va.student_id, va.subject)
    where v.first_rank = 1 and va.last_rank = 1 and v.score<va.score