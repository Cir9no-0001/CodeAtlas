// Jump Game
// https://leetcode.com/problems/jump-game
// difficulty: medium
// first_seen: 2026-11-02 10:31:15 EST
// runtime: 1ms

/*
Notes:

*/

class Solution {
public:
    bool canJump(vector<int>& nums) {
        int big_hop = 0;
        
        for (int i = 0; i < nums.size(); i++){
            if (i > big_hop){
                return false;
            }
            
            big_hop = max(big_hop, i + nums[i]);
            
            if (big_hop >= nums.size()-1){
                return true;
            }
        }
        
        return false;
    }
};