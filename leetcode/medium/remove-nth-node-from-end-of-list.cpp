// Remove Nth Node From End of List
// https://leetcode.com/problems/remove-nth-node-from-end-of-list
// difficulty: medium
// first_seen: 2026-09-28 14:07:57 EDT
// runtime: 0ms

/*
Notes:

*/

class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode* front = head;
        ListNode* back = head;
        int diff = 0;

        while (front != nullptr){ 
            // n+1 since back must stop 1 node before one u need to delete
            if (diff < n+1){
                front = front -> next;
                diff++;
            }else{
                back = back -> next;
                front = front -> next;
            }
        }

        // Edge case when n is the length of the list
        if (diff == n && front == nullptr && back == head) {
            ListNode* newHead = head->next;
            delete head;
            return newHead;
        }

        ListNode* Del = back->next;
        back->next = back->next->next;
        delete Del;

        return head;
    }
};