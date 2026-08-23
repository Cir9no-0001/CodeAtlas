-- Recyclable and Low Fat Products
-- https://leetcode.com/problems/recyclable-and-low-fat-products
-- difficulty: easy
-- first_seen: 2026-08-22 21:48:37 EDT
-- runtime: 572ms

/*
Notes:
Hint: just filter with where
*/

select p.product_id
from Products p
where p.low_fats = 'Y' and p.recyclable = 'Y'