-- Invalid Tweets
-- https://leetcode.com/problems/invalid-tweets
-- difficulty: easy
-- first_seen: 2026-08-05 10:14:17 EDT
-- runtime: 592ms

/*
Notes:

*/


select t.tweet_id
from Tweets t
where length(t.content)>15