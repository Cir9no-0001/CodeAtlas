// Maximum Depth of Binary Tree
// https://leetcode.com/problems/maximum-depth-of-binary-tree
// difficulty: easy
// first_seen: 2026-10-05 13:12:28 EDT
// runtime: 0ms

/*
Notes:
Traverse the left and right subtrees recursively, using a nullptr node as the base case.
At each node, determine whether the left or right subtree has a greater depth, and return
that maximum value plus one to account for the current node. [TC: O(N), SC: O(N)]
*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left),
 * right(right) {}
 * };
 */
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (!root)
            return 0;
        int left = maxDepth(root->left);
        int right = maxDepth(root->right);
        return max(left, right) + 1;
    }
};