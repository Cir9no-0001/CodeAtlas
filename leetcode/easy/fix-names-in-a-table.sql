-- Fix Names in a Table
-- https://leetcode.com/problems/fix-names-in-a-table
-- difficulty: easy
-- first_seen: 2026-08-04 06:02:24 EDT
-- runtime: 838ms

/*
Notes:
Hint: split each name into head and tail using substring, uppercase the head, lowercase
the tail, then concat both for the correct name format. [TC: O(NlogN), 1 pass]
*/

select 
    u.user_id,
    concat(upper(substring(u.name, 1, 1)), lower(substring(u.name, 2))) as 'name'
from Users u
order by u.user_id asc