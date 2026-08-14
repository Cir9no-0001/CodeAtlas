// Two Sum
// https://leetcode.com/problems/two-sum
// difficulty: easy
// first_seen: 2026-08-13 23:09:02 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> numMap;
        int n = nums.size();

        for (int i = 0; i < n; i++) {
            int complement = target - nums[i];
            if (numMap.count(complement)) {
                return {numMap[complement], i};
            }
            numMap[nums[i]] = i;
        }

        return {}; // No solution found
    }
};