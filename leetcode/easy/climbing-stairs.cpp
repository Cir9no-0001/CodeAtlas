// Climbing Stairs
// https://leetcode.com/problems/climbing-stairs
// difficulty: easy
// first_seen: 2026-08-28 05:54:56 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int climbStairs(int n) {
        if (n <= 3) return n;

        int bk1 = 3;
        int bk2 = 2;
        int cur = 0;

        for (int i = 3; i < n; i++) {
            cur = bk1 + bk2;
            bk2 = bk1;
            bk1 = cur;
        }

        return cur;        
    }
};