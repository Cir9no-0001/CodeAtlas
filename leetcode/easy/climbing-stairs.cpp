// Climbing Stairs
// https://leetcode.com/problems/climbing-stairs
// difficulty: easy
// first_seen: 2026-08-28 05:54:56 EDT
// runtime: 0ms

/*
Notes:
Hint: Use pen and paper for the first 4-5 to see the pattern. Once the pattern is
obvious, establish the minimum number of base cases and approach the problem using a for
loop according to the pattern. [TC: O(n)]
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