// Best Time to Buy and Sell Stock II
// https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii
// difficulty: medium
// first_seen: 2026-11-02 10:31:16 EST
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int profit = 0;
        for (int i = 0; i < prices.size() - 1; i++){
            if (prices[i] < prices[i+1]){
                profit += prices[i+1] - prices[i];
            }
        }
        
        return profit;
    }
};