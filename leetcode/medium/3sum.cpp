// 3Sum
// https://leetcode.com/problems/3sum
// difficulty: medium
// first_seen: 2026-08-26 20:31:49 EDT
// runtime: 51ms

/*
Notes:

*/

class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> ans;

        for (int i = 0; i < nums.size(); i++){
            if (i > 0 && nums[i] == nums[i-1]){
                continue;
            }

            int j = i + 1;
            int k = nums.size() - 1;

            while (j<k){
                int sum = nums[i] + nums[j] + nums[k];
                if (sum == 0){
                    ans.push_back({nums[i],nums[j],nums[k]});
                    j++;

                    while (nums[j] == nums[j-1] && j < k) {
                        j++;
                    }

                } else if (sum > 0){
                    k--;
                } else{
                    j++;
                }
            }

        }

        return ans;
    
    }
};