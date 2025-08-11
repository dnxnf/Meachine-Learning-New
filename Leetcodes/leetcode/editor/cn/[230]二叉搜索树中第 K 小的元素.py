# 给定一个二叉搜索树的根节点 root ，和一个整数 k ，请你设计一个算法查找其中第 k 小的元素（从 1 开始计数）。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [3,1,4,null,2], k = 1
# 输出：1
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [5,3,6,2,4,null,null,1], k = 3
# 输出：3
#  
# 
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中的节点数为 n 。 
#  1 <= k <= n <= 10⁴ 
#  0 <= Node.val <= 10⁴ 
#  
# 
#  
# 
#  进阶：如果二叉搜索树经常被修改（插入/删除操作）并且你需要频繁地查找第 k 小的值，你将如何优化算法？ 
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 1000 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest1(self, root: Optional[TreeNode], k: int) -> int:
        def inorder(node: Optional[TreeNode]) -> List[int]:
            if not node:
                return []
            return inorder(node.left) + [node.val] + inorder(node.right)

        return inorder(root)[k - 1]

    def kthSmallest2(self, root: Optional[TreeNode], k: int) -> int:
        res = []

        def inorder(node: Optional[TreeNode]) -> List[int]:
            if not node:
                return []
            inorder(node.left)
            res.append(node.val)
            inorder(node.right)

        inorder(root)
        return res[k - 1]

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        while root or stack:
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            k -= 1
            if k == 0:
                return root.val
            root = root.right


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(4)
    root.left.right = TreeNode(2)
    root.left.left = TreeNode(0)
    print(solution.kthSmallest(root, 2))
