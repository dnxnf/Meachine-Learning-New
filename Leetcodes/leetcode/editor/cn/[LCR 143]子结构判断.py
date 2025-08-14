#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 给定两棵二叉树 tree1 和 tree2，判断 tree2 是否以 tree1 的某个节点为根的子树具有 相同的结构和节点值 。 注意，空树 不会是以
# tree1 的某个节点为根的子树具有 相同的结构和节点值 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 
#  
# 
#  
# 输入：tree1 = [1,7,5], tree2 = [6,1]
# 输出：false
# 解释：tree2 与 tree1 的一个子树没有相同的结构和节点值。
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：tree1 = [3,6,7,1,8], tree2 = [6,1]
# 输出：true
# 解释：tree2 与 tree1 的一个子树拥有相同的结构和节点值。即 6 - > 1。 
# 
#  
# 
#  提示： 
# 
#  0 <= 节点个数 <= 10000 
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 830 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def isSubStructure(self, A: Optional[TreeNode], B: Optional[TreeNode]) -> bool:
        if not B:  # 题目规定空树不是任何树的子结构
            return False

        def dfs(root1, root2):
            # 如果B已经遍历完了，说明匹配成功
            if not root2:
                return True
            # 如果A遍历完了但B还有节点，匹配失败
            if not root1:
                return False
            # 当前节点值相等时，继续匹配左右子树
            if root1.val == root2.val:
                return dfs(root1.left, root2.left) and dfs(root1.right, root2.right)
            # 当前节点值不等时，返回False
            return False

            # 在A中寻找与B根节点匹配的节点

        def find_root(A, B):
            if not A:
                return False
            # 如果找到匹配的根节点，检查子树
            if A.val == B.val and dfs(A, B):
                return True
            # 继续在左右子树中寻找
            return find_root(A.left, B) or find_root(A.right, B)

        return find_root(A, B)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    tree1 = TreeNode(1, TreeNode(7), TreeNode(5))
    tree2 = TreeNode(7)
    print(solution.isSubStructure(tree1, tree2))