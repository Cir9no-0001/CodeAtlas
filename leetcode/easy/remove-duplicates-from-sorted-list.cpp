// Remove Duplicates from Sorted List
// https://leetcode.com/problems/remove-duplicates-from-sorted-list
// difficulty: easy
// first_seen: 2026-10-17 21:36:04 EDT
// runtime: 0ms

/*
Notes:

*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        ListNode* ans = head;
        
        while (head && head -> next){
            if (head->val == head->next->val){
                head->next = head->next->next;
            }else{
                head = head->next;
            }
        }
        
        return ans;
    }
};