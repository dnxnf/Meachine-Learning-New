# 给定一个二叉树 root ，返回其最大深度。 
# 
#  二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数。 
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
# 输入：root = [3,9,20,null,null,15,7]
# 输出：3
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [1,null,2]
# 输出：2
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点的数量在 [0, 10⁴] 区间内。 
#  -100 <= Node.val <= 100 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 1983 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
# favour 递归,最大深度
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth1(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        tmax = 0
        if root.left:
            tmax = max(tmax, self.maxDepth(root.left))
        if root.right:
            tmax = max(tmax, self.maxDepth(root.right))
        return tmax + 1

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        root1 = self.maxDepth(root.left)
        root2 = self.maxDepth(root.right)
        return max(root1, root2) + 1


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
