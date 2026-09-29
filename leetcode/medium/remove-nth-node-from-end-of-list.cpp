// Remove Nth Node From End of List
// https://leetcode.com/problems/remove-nth-node-from-end-of-list
// difficulty: medium
// first_seen: 2026-09-28 14:07:57 EDT
// runtime: 0ms

/*
Notes:
Hint: Use a sliding window/two pointer approach to traverse the linked list while
maintaining a gap of n+1 from head to tail so the tail lands on the node before the one
you want to delete. If the list's total length equals n, the back pointer won't advance
past the head, meaning you must manually handle removing the first node as an edge case.
[TC: O(N), SC: O(1)]
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