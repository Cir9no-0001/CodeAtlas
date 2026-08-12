-- Palindrome Number
-- https://leetcode.com/problems/palindrome-number
-- difficulty: easy
-- first_seen: 2026-08-12 18:40:14 EDT
-- runtime: 7ms

/*
Notes:

*/

class Solution(object):
    def isPalindrome(self, x):
        x = str(x)
        return x == x[::-1]