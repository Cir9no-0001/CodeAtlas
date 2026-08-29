// Pascal's Triangle
// https://leetcode.com/problems/pascals-triangle
// difficulty: easy
// first_seen: 2026-08-29 02:05:11 EDT
// runtime: 0ms

/*
Notes:
Hint: Use the previous row stash method to keep the values of the previous row to build
the current row and push it into the answer array. Loop to create each new row,
initializing it completely with 1s and sizing it to match the current row number. Then,
loop from index 1 to the second-to-last index, overwriting the 1s with the sum of the
values at the current index and the previous index from the previous row. Finally, push
the completed row into the 2D array answer and shift the previous frame. [TC: O(n^2)]
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