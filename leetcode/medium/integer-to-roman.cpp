// Integer to Roman
// https://leetcode.com/problems/integer-to-roman
// difficulty: medium
// first_seen: 2026-08-23 19:03:35 EDT
// runtime: 0ms

/*
Notes:
Hint: Create two arrays to store the values and corresponding strings to append in order.
Use a for loop to scan through all 13 potential letters to add, and while the number is
greater than the corresponding value, append the corresponding string to the final answer
num/value[i] times. Then set the number to the number modulo the corresponding value. DO
NOT use .append since some corresponding letters to append are strings, not chars, while
.append expects chars. [TC: O(1)]
*/

class Solution {
public:
    string intToRoman(int num) {
        string roman = "";
        const string letter[13]={"M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"};
        const int value[13]={1000,900,500,400,100,90,50,40,10,9,5,4,1};

        for (int i = 0; i < 13; i++){
            while (num / value[i] > 0){
                for (int j = 0; j < num/value[i]; j++) {
                    roman += letter[i];
                }

                num = num % value[i];
            }
        }

        return roman;

    }
};