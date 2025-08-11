# 给定一个二叉树，判断它是否是 平衡二叉树 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [3,9,20,null,null,15,7]
# 输出：true
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [1,2,2,3,3,null,null,4,4]
# 输出：false
#  
# 
#  示例 3： 
# 
#  
# 输入：root = []
# 输出：true
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中的节点数在范围 [0, 5000] 内 
#  -10⁴ <= Node.val <= 10⁴ 
#  
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 1610 👎 0

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
        # 判断每个节点是否平衡，后续遍历即可，得到左右子树的深度,一旦不平衡就结束
        # 全局变量
        self.res = True

        def height(node: TreeNode):
            if not node:
                return 0
            # num = node.val
            left = height(node.left)
            right = height(node.right)
            print(left, right)
            if abs(left - right) > 1:
                self.res = False
            return max(left, right) + 1

        height(root)
        return bool(self.res)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.left.left.left = TreeNode(6)
    root.left.left.right = TreeNode(7)
    print(solution.isBalanced(root))
