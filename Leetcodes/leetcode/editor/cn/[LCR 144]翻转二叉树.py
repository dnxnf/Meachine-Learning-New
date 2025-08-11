# 给定一棵二叉树的根节点 root，请左右翻转这棵二叉树，并返回其根节点。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [5,7,9,8,3,2,4]
# 输出：[5,9,7,4,2,3,8]
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
#  
# 
#  注意：本题与主站 226 题相同：https://leetcode-cn.com/problems/invert-binary-tree/ 
# 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 397 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def flipTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        #         递归，相信左右能翻转
        def dfs(node):
            if not node:
                return
            left = dfs(node.left)
            right = dfs(node.right)
            node.left, node.right = right, left
            return node
        return dfs(root)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
