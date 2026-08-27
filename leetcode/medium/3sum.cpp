// 3Sum
// https://leetcode.com/problems/3sum
// difficulty: medium
// first_seen: 2026-08-26 20:31:49 EDT
// runtime: 51ms

/*
Notes:
Hint: Sort the array from least to greatest, then iterate through it using a for loop. In
the for loop, make sure each run starts with a distinct, fixed first number to prevent
duplicate triplets (skip if it is the same as the previous loop). Use a two-pointer
approach with a while loop to find the other two numbers that work with the first number.
Start the second number at first number + 1 and the third at the tail. When the triplet
adds up to 0, make sure the moving second number is distinct for every triplet with a
fixed first number; otherwise, move the pointers according to the sum. [TC: O(N^2)]
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