// Valid Parentheses
// https://leetcode.com/problems/valid-parentheses
// difficulty: easy
// first_seen: 2026-08-27 22:39:48 EDT
// runtime: 0ms

/*
Notes:
Hint: Use a stack and peel the string from the innermost brackets out with a for loop for
each char in the string. Let the opening brackets stack, and when a closing bracket shows
up, it should match the most recent opening bracket; if not, return false. Also, make
sure that the first bracket isn't a closing bracket. Once the for loop goes through all
the chars in the string, the stack should be empty and return that state. [TC: O(N)]
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