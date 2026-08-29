// Remove Duplicates from Sorted Array
// https://leetcode.com/problems/remove-duplicates-from-sorted-array
// difficulty: easy
// first_seen: 2026-08-28 23:58:21 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        if (nums.empty()){
            return 0;
        }
        
        int size = 1;

        for (int i = 1; i < nums.size(); i++){
            if (nums[i]>nums[i-1]){
                nums[size] = nums[i];
                size++;
            }
        }

        return size;
    }
};