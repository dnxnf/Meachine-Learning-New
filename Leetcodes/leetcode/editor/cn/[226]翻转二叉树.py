# 给你一棵二叉树的根节点 root ，翻转这棵二叉树，并返回其根节点。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [4,2,7,1,3,6,9]
# 输出：[4,7,2,9,6,3,1]
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：root = [2,1,3]
# 输出：[2,3,1]
#  
# 
#  示例 3： 
# 
#  
# 输入：root = []
# 输出：[]
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数目范围在 [0, 100] 内 
#  -100 <= Node.val <= 100 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 1963 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree1(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        # 翻转左右子树
        # 右子树赋值给左子树，左子树赋值给右子树,直接在原来树上交换

        root.left, root.right = root.right, root.left
        # 翻转之后，下层子树接着翻转
        if root.left:
            self.invertTree1(root.left)
        if root.right:
            self.invertTree1(root.right)
        return root

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return root

        def reverse(node):
            # if node.left or node.right:
            #     node.left, node.right = node.right, node.left
            node.left, node.right = node.right, node.left
            if node.right:
                reverse(node.right)
            if node.left:
                reverse(node.left)
        reverse(root)
        return root

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
