-- Group Sold Products By The Date
-- https://leetcode.com/problems/group-sold-products-by-the-date
-- difficulty: easy
-- first_seen: 2026-07-24 23:20:34 EDT
-- runtime: 523ms

/*
Notes:
Hint: remember that only distinct pairs of (sell_date, product) are valid. Sort
lexicographically using order by product asc in the group_concat. [TC: O(n), 1 pass]
*/

select 
    a.sell_date,
    count(distinct a.product) as 'num_sold',
    group_concat(distinct product order by product asc separator ',') as 'products'
from Activities a
group by a.sell_date