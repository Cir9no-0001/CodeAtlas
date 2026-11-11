// Longest Palindrome
// https://leetcode.com/problems/longest-palindrome
// difficulty: easy
// first_seen: 2026-11-10 22:13:33 EST
// runtime: 1ms

/*
Notes:

*/

class Solution {
public:
    int longestPalindrome(string s) {
        sort(s.begin(), s.end());
        bool odd = false;
        int count = 0;
        
        for(int i = 1; i <= s.size(); i++){
            if (s[i] == s[i-1]){
                count+=2;
                i++;
            } else {odd = true;}
        }
        
        return (odd) ? ++count: count;
    }
};