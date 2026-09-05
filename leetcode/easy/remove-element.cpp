// Remove Element
// https://leetcode.com/problems/remove-element
// difficulty: easy
// first_seen: 2026-09-05 16:25:29 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int k = 0;

        for (int i = 0; i < nums.size(); i++){
            if (nums[i] != val){
                nums[k] = nums[i];
                k++;
            }
        }

        return k;
    }
};