// Array Partition
// https://leetcode.com/problems/array-partition
// difficulty: easy
// first_seen: 2026-11-09 23:49:37 EST
// runtime: 11ms

/*
Notes:

*/

class Solution {
public:
    int arrayPairSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int sum = 0;
        for (int i = 0; i < nums.size(); i+=2){
            sum += nums[i];
        }
        
        return sum;
    }
};