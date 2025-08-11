# 实现一个函数，检查二叉树是否平衡。在这个问题中，平衡树的定义如下：任意一个节点，其两棵子树的高度差不超过 1。 
#  
# 示例 1：
# 
#  
# 给定二叉树 [3,9,20,null,null,15,7]
#     3
#    / \
#   9  20
#     /  \
#    15   7
# 返回 true 。 
# 
# 示例 2：
# 
#  
# 给定二叉树 [1,2,2,3,3,null,null,4,4]
#       1
#      / \
#     2   2
#    / \
#   3   3
#  / \
# 4   4
# 返回 false 。 
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 113 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        # depth = 1
        res = True

        # 获得左右子树的高度，并作差
        def dfs(node):
            if not node:
                return 0
            nonlocal res
            # 左子树深度和右子树深度
            depth1 = 1 + dfs(node.left)
            depth2 = 1 + dfs(node.right)

            if abs(depth1 - depth2) > 1:
                res = False
            return max(depth1, depth2)

        dfs(root)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    # solution = Solution()
    solution = Solution()
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.left.left.left = TreeNode(6)
    root.left.left.right = TreeNode(7)
    print(solution.isBalanced(root))
