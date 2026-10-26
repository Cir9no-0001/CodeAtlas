// Median of Two Sorted Arrays
// https://leetcode.com/problems/median-of-two-sorted-arrays
// difficulty: hard
// first_seen: 2026-10-26 15:29:30 EDT
// runtime: 8ms

/*
Notes:

*/

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int p1 = 0;
        int p2 = 0;
        vector<int> merged;
        
        while (p1<nums1.size() && p2<nums2.size()){
            if (nums1[p1]<=nums2[p2]){
                merged.push_back(nums1[p1]);
                p1++;
            }else{
                merged.push_back(nums2[p2]);
                p2++;
            }
        }
        
        while (p1 < nums1.size()) {
            merged.push_back(nums1[p1]);
            p1++;
        }

        while (p2 < nums2.size()) {
            merged.push_back(nums2[p2]);
            p2++;
        }
        
        return ((merged.size()-1)%2==0) ? merged[(merged.size()-1)/2]: (merged[merged.size()/2]+merged[merged.size()/2 -1])/2.0;
    }
};