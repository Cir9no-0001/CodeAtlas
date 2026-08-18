// Longest Common Prefix
// https://leetcode.com/problems/longest-common-prefix
// difficulty: easy
// first_seen: 2026-08-17 20:24:37 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        string prefix = "";
        sort (strs.begin(), strs.end());
        
        int n = strs.size();
        string first = strs[0], last = strs [n-1];

        for (int i = 0; i < min (first.size(), last.size()); i++){
            if (first[i] != last[i]){
                return prefix;
            }
            prefix += first[i];
        }
        return prefix;
    }
};