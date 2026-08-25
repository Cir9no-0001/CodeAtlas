// Container With Most Water
// https://leetcode.com/problems/container-with-most-water
// difficulty: medium
// first_seen: 2026-08-24 21:16:53 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    int maxArea(vector<int>& height) {
        int p1 = 0;
        int p2 = height.size() - 1;
        int area = 0;

        for (int i = 0; i < height.size(); i++){
            int currentArea = min(height[p1], height[p2]) * (p2 - p1);
            area = max(area, currentArea);

            if (height[p1] > height[p2] && p1 != p2){
                p2 -= 1;
            }else if (p1 != p2){
                p1 += 1;
            }
        }

        return area;
    }
};