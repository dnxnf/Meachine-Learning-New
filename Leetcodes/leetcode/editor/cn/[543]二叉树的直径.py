# 给你一棵二叉树的根节点，返回该树的 直径 。 
# 
#  二叉树的 直径 是指树中任意两个节点之间最长路径的 长度 。这条路径可能经过也可能不经过根节点 root 。 
# 
#  两节点之间路径的 长度 由它们之间边数表示。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [1,2,3,4,5]
# 输出：3
# 解释：3 ，取路径 [4,2,1,3] 或 [5,2,1,3] 的长度。
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [1,2]
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数目在范围 [1, 10⁴] 内 
#  -100 <= Node.val <= 100 
#  
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 1740 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree1(self, root: TreeNode) -> int:
        # if not root:
        #     return 0
        ans = 1

        def depth(node):
            if not node:
                return 0
            nonlocal ans
            left = depth(node.left)
            right = depth(node.right)
            ans = max(left + right + 1, ans)
            return 1 + max(left, right)

        depth(root)
        return ans - 1

    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        # 手写版，得到左右子树的深度相加-2
        # if not root:
        #     return 0
        res = 0

        def depth(node):
            nonlocal res
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            res = max(left + right + 1, res)
            return 1 + max(left, right)

        depth(root)
        print(res)
        return res


# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(solution.diameterOfBinaryTree(root))
