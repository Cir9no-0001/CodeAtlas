// Assign Cookies
// https://leetcode.com/problems/assign-cookies
// difficulty: easy
// first_seen: 2026-11-09 15:07:45 EST
// runtime: 8ms

/*
Notes:

*/

class Solution {
public:
    int findContentChildren(vector<int>& g, vector<int>& s) {
        sort(g.begin(), g.end());
        sort(s.begin(), s.end());
        
        int child = 0;
        int food = 0;
        
        while (food < s.size() && child < g.size()){
            if (s[food] >= g[child]){
                child++;
                food++;
            }else{
                food++;
            }
        }
        
        return child;
        
    }
};