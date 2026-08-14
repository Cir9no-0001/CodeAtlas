-- Odd and Even Transactions
-- https://leetcode.com/problems/odd-and-even-transactions
-- difficulty: medium
-- first_seen: 2026-07-30 04:35:57 EDT
-- runtime: 301ms

/*
Notes:
Hint: addition problem with modulo and case/if. [TC: O(N), 1 pass]
*/

select
    t.transaction_date,
    sum(if(t.amount%2=1, t.amount, 0)) as 'odd_sum',
    sum(if(t.amount%2=0, t.amount, 0)) as 'even_sum'
from transactions t
group by t.transaction_date
order by t.transaction_date asc