-- Find Users With Valid E-Mails
-- https://leetcode.com/problems/find-users-with-valid-e-mails
-- difficulty: easy
-- first_seen: 2026-08-01 20:11:01 EDT
-- runtime: 744ms

/*
Notes:

*/


select *
from Users u
where regexp_like(u.mail, '^[a-zA-Z][a-zA-Z0-9._-]*@leetcode[.]com$', 'c')