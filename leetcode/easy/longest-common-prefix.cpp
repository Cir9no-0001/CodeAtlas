// Longest Common Prefix
// https://leetcode.com/problems/longest-common-prefix
// difficulty: easy
// first_seen: 2026-08-17 16:48:01 EDT
// runtime: 0ms

/*
Notes:
Hint: Sort the big array of words so that the first and last elements are the most
dissimilar words, then extract the first and last words. Use a for loop to compare the
characters of the two elements, add any matching characters to the prefix string, and
when it doesn't, just return the current prefix. [TC: O(nLogn)]
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