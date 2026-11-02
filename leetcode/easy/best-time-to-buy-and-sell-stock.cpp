// Best Time to Buy and Sell Stock
// https://leetcode.com/problems/best-time-to-buy-and-sell-stock
// difficulty: easy
// first_seen: 2026-11-02 09:29:18 EST
// runtime: 1ms

/*
Notes:

*/

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int buy = INT_MAX;
        int profit = 0;
        
        for (int i = 0; i < prices.size(); i++){
            if (prices[i]<buy){
                buy = prices[i];
            }else if (prices[i] - buy > profit){
                profit = prices[i] - buy;
            }
        }
        
        return profit;
    }
};