// Pascal's Triangle
// https://leetcode.com/problems/pascals-triangle
// difficulty: easy
// first_seen: 2026-08-29 02:05:11 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> ans;
        vector<int> prev;

        for (int i = 1; i <= numRows; i++){
            vector<int> curr(i, 1);

            for (int j = 1; j < i-1; j++){
                curr[j] = prev[j-1] + prev[j];
            }

            ans.push_back(curr);
            prev=curr;
        }

        return ans;
    }
};