// Length of Last Word
// https://leetcode.com/problems/length-of-last-word
// difficulty: easy
// first_seen: 2026-10-04 22:27:55 EDT
// runtime: 0ms

/*
Notes:
Hint: Traverse the string backwards, filtering out all whitespace and counting the chars
of the first word you see until another whitespace appears, then stop. [TC: O(N), SC:
O(1)]
*/

class Solution {
public:
    int lengthOfLastWord(string s) {
        int i = s.size() - 1;
        int len = 0;
        
        while ( i >= 0 && s[i] == ' ' ){
            i--;
        }
        
        while ( i >= 0 && s[i] != ' '){
            len++;
            i--;
        }
        
        return len;
    }
};