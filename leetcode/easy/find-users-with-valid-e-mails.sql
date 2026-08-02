-- Find Users With Valid E-Mails
-- https://leetcode.com/problems/find-users-with-valid-e-mails
-- difficulty: easy
-- first_seen: 2026-08-01 20:11:01 EDT
-- runtime: 744ms

/*
Notes:
Hint: use regexp_like to get case sensitivity for the suffix, or use an extra like
binary. Watch out for the period in the suffix, which is a wildcard, so put it in square
brackets. [TC: O(N), 1 pass]
*/


select *
from Users u
where regexp_like(u.mail, '^[a-zA-Z][a-zA-Z0-9._-]*@leetcode[.]com$', 'c')