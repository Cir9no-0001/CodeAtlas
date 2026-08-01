-- Customer Who Visited but Did Not Make Any Transactions
-- https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions
-- difficulty: easy
-- first_seen: 2026-07-30 03:17:06 EDT
-- runtime: 1320ms

/*
Notes:
Hint: join the two tables, then filter out the ones that have ID values in both tables.
Group and sum the rest accordingly. [TC: O(V+T), 2 passes]
*/


select 
    v.customer_id,
    ifnull(count(v.visit_id), 0) as 'count_no_trans'
from Visits v
left join Transactions t
    on v.visit_id = t.visit_id
    where t.visit_id is null
group by v.customer_id