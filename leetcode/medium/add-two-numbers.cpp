// Add Two Numbers
// https://leetcode.com/problems/add-two-numbers
// difficulty: medium
// first_seen: 2026-08-15 22:40:32 EDT
// runtime: 0ms

/*
Notes:
Hint: while the values of both lists are not both null or carried value is not 0, extract
the two pointer values and if null, set them to 0. Add them and the carry value for the
sum then modulo by 10 to get the ones place digit and set carry value according to sum.
Append new digit value to tail and advance all pointers
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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* head = new ListNode{0};
        ListNode* tail = head;
        int c = 0;

        while (l1 != nullptr || l2 != nullptr || c != 0){
            int n1 = (l1 != nullptr) ? l1 -> val : 0;
            int n2 = (l2 != nullptr) ? l2 -> val : 0;

            int sum = n1 + n2 + c;
            int digit = sum % 10;
            c = (sum > 9) ? 1 : 0;

            ListNode* newNode = new ListNode(digit);
            tail -> next = newNode;
            tail = tail -> next;
            
            l1 = (l1 != nullptr) ? l1 -> next : nullptr;
            l2 = (l2 != nullptr) ? l2 -> next : nullptr;
        }

        ListNode* result = head -> next;
        delete head;
        return result;
    }
};