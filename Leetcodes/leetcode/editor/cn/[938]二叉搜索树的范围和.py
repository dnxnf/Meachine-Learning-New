# 给定二叉搜索树的根结点 root，返回值位于范围 [low, high] 之间的所有结点的值的和。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [10,5,15,3,7,null,18], low = 7, high = 15
# 输出：32
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [10,5,15,3,7,13,18,1,null,6], low = 6, high = 10
# 输出：23
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数目在范围 [1, 2 * 10⁴] 内 
#  1 <= Node.val <= 10⁵ 
#  1 <= low <= high <= 10⁵ 
#  所有 Node.val 互不相同 
#  
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 395 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rangeSumBST1(self, root: Optional[TreeNode], low: int, high: int) -> int:
        # 没有剪枝的普通方法
        res = []

        def dfs(node):
            if not node:
                return
            if node.val >= low and node.val <= high:
                res.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return sum(res)

    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        #         包括剪枝
        res = []
        def dfs(node):
            if not node:
                return
            if node.val >= low and node.val <= high:
                res.append(node.val)
            if node.val > high:
                dfs(node.left)
            elif node.val < low:
                dfs(node.right)
            else:
                dfs(node.left)
                dfs(node.right)

        dfs(root)
        return sum(res)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(18)
    root.left.left.left = TreeNode(1)
    root.left.right.right = TreeNode(6)
    print(solution.rangeSumBST(root, 6, 10))
