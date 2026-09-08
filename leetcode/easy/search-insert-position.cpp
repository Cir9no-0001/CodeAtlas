// Search Insert Position
// https://leetcode.com/problems/search-insert-position
// difficulty: easy
// first_seen: 2026-09-07 22:54:18 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int head = nums.size()-1;
        int tail = 0;
        
        while (head >= tail){
            int mid = tail + (head - tail)/2;
            
            if (nums[mid] == target){
                return mid;
            } else if (nums[nums.size()-1] < target){
                return nums.size();
            } else if (nums[0] > target){
                return 0;
            } else if (nums[head]>target && nums[tail]<target && head-tail==1){
                return tail+1;
            } else if (nums[mid] < target){
                tail = mid + 1;
            } else if (nums[mid] > target){
                head = mid - 1;
            } 
            
        }
        return tail;
    }
};