-- Bank Account Summary II
-- https://leetcode.com/problems/bank-account-summary-ii
-- difficulty: easy
-- first_seen: 2026-07-26 22:35:45 EDT
-- runtime: 815ms

/*
Notes:
Hint: group by account number and filter using having and sum [TC: O(N+M), 1 pass]
*/

select 
    u.name,
    sum(t.amount) as 'balance'
from Transactions t
inner join Users u
on t.account = u.account
group by t.account
having sum(t.amount)>10000