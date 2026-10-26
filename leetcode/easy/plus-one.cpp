// Plus One
// https://leetcode.com/problems/plus-one
// difficulty: easy
// first_seen: 2026-10-17 21:36:05 EDT
// runtime: 0ms

/*
Notes:
Hint: Add 1 to the last element of the array. If a carry is generated (digit > 9), reset
it to 0 and move left to increment the next digit. Repeat this carry process until no
digit exceeds 9, or until you cross index 0 (e.g., 999 to 1000), where you insert a 1 at
the very front of the array. [TC: O(N), SC: O(N)]
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