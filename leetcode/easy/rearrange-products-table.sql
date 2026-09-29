-- Rearrange Products Table
-- https://leetcode.com/problems/rearrange-products-table
-- difficulty: easy
-- first_seen: 2026-09-28 22:49:12 EDT
-- runtime: 588ms

/*
Notes:

*/

select p.product_id, 'store1' as store, p.store1 as 'price'
from Products p
where p.store1 is not null

union all

select p.product_id, 'store2' as store, p.store2 as 'price'
from Products p
where p.store2 is not null

union all

select p.product_id, 'store3' as store, p.store3 as 'price'
from Products p
where p.store3 is not null