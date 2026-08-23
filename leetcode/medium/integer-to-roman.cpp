// Integer to Roman
// https://leetcode.com/problems/integer-to-roman
// difficulty: medium
// first_seen: 2026-08-23 19:03:35 EDT
// runtime: 0ms

/*
Notes:

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