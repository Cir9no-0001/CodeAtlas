// 3Sum Closest
// https://leetcode.com/problems/3sum-closest
// difficulty: medium
// first_seen: 2026-08-26 21:15:07 EDT
// runtime: 15ms

/*
Notes:
Hint: Sort the array from least to greatest, then iterate through it using a for loop.
For each run, use a two-pointer approach with a left pointer starting at the first number
+ 1 and a right pointer starting at the tail. Calculate the triplet sum and update the
best answer if it is closer to the target than the current answer. Then move the pointers
according to the sum: decrement the right pointer if the sum is greater than the target;
otherwise, increment the left pointer. [TC: O(N^2)]
*/

class Solution {
public:
    int threeSumClosest(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int ans = nums[0] + nums[1] + nums[2];

        for (int i = 0; i < nums.size()-2; i++){
            int j = i + 1;
            int k = nums.size() - 1;

            while (j<k){
                int sum = nums[i] + nums[j] + nums[k];
                ans = (abs(target-sum)<abs(target-ans)) ? sum : ans;

                if (sum > target){
                    k--;
                } else{
                    j++;
                }
            }

        }

        return ans;
    }
};