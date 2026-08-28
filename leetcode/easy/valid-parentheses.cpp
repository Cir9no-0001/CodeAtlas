// Valid Parentheses
// https://leetcode.com/problems/valid-parentheses
// difficulty: easy
// first_seen: 2026-08-27 22:39:48 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    bool isValid(string s) {
        stack <char> brst;
        
        for (char ch : s){
            if (ch == '(' || ch == '[' || ch == '{'){
                brst.push(ch);
            }else{
                if (brst.empty()) {return false;}

                char top = brst.top();
                brst.pop();

                if (ch == ')' && top != '(') {return false;}
                if (ch == ']' && top != '[') {return false;}
                if (ch == '}' && top != '{') {return false;}
            }
        }

        return (brst.empty());
    }
};