-- Daily Leads and Partners
-- https://leetcode.com/problems/daily-leads-and-partners
-- difficulty: easy
-- first_seen: 2026-08-06 08:54:21 EDT
-- runtime: 678ms

/*
Notes:

*/


select 
    d.date_id, 
    d.make_name,
    count(distinct d.lead_id) as 'unique_leads', 
    count(distinct d.partner_id) as 'unique_partners'
from DailySales d
group by d.date_id, d.make_name