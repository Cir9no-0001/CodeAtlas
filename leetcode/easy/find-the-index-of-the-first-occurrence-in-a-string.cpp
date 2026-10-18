// Find the Index of the First Occurrence in a String
// https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string
// difficulty: easy
// first_seen: 2026-10-17 21:36:05 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int strStr(string haystack, string needle) {
        int head = needle.size()-1;
        int tail = 0;
        
        while (head<haystack.size()){
            for (int i = 0; i<needle.size(); i++){
                if (haystack[tail+i] != needle[i]){
                    break;
                }
                
                if (i==needle.size()-1){
                    return tail;
                }
            }
            tail++;
            head++;
        }
        
        return -1;
    }
};