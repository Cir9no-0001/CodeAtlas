// 3Sum Closest
// https://leetcode.com/problems/3sum-closest
// difficulty: medium
// first_seen: 2026-08-26 21:15:07 EDT
// runtime: 15ms

/*
Notes:

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