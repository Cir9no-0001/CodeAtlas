// Plus One
// https://leetcode.com/problems/plus-one
// difficulty: easy
// first_seen: 2026-10-17 21:36:05 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        int i = digits.size()-1;
        
        digits[i]++;
        while (digits[i] > 9 && i >= 0){
            digits[i] = 0;
            i--;
            if (i == -1){
                digits.insert(digits.begin(), 1);
                break;
            }
            else{
                digits[i]++;
            }
        }
        
        return digits;
    }
};