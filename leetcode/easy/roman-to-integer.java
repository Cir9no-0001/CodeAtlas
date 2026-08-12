-- Roman to Integer
-- https://leetcode.com/problems/roman-to-integer
-- difficulty: easy
-- first_seen: 2026-08-12 19:00:31 EDT
-- runtime: 5ms

/*
Notes:

*/

import java.util.*;

class Solution {
    public int romanToInt(String s) {
        Map<Character, Integer> map = Map.of(
            'I', 1, 'V', 5, 'X', 10,
            'L', 50, 'C', 100, 'D', 500, 'M', 1000
        );

        int result = 0;
        for (int i = 0; i < s.length(); i++) {
            int curr = map.get(s.charAt(i));
            int next = (i + 1 < s.length()) ? map.get(s.charAt(i + 1)) : 0;

            if (curr < next) {
                result -= curr;
            } else {
                result += curr;
            }
        }

        return result;
    }
}