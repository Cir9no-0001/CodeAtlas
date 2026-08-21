// String to Integer (atoi)
// https://leetcode.com/problems/string-to-integer-atoi
// difficulty: medium
// first_seen: 2026-08-21 19:51:56 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int myAtoi(string s) {
        int i = 0;
        int sign = 1;
        long ans = 0;

        while (s[i] == ' ' && i < s.length()){
            i++;
        }

        if (s[i] == '-'){
            sign = -1;
            i++;
        }else if (s[i] == '+'){
            sign = 1;
            i++;
        }

        while (isdigit(s[i]) && i < s.length()){
            ans = ans*10+(s[i]-'0');

            if (ans*sign>INT_MAX){
                return INT_MAX;
            }else if (ans*sign<INT_MIN){
                return INT_MIN;
            }

            i++;
        }

        return (sign*ans);
    }
};