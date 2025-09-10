# 设计一个算法，找出二叉搜索树中指定节点的“下一个”节点（也即中序后继）。 
# 
#  如果指定节点没有对应的“下一个”节点，则返回null。 
# 
#  示例 1： 
# 
#  
# 输入：root = [2,1,3], p = 1
# 
#   2
#  / \
# 1   3
# 
# 输出：2 
# 
#  示例 2： 
# 
#  
# 输入：root = [5,3,6,2,4,null,null,1], p = 6
# 
#       5
#      / \
#     3   6
#    / \
#   2   4
#  /   
# 1
# 
# 输出：null 
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 240 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def inorderSuccessor(self, root: TreeNode, p: TreeNode) -> TreeNode:
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)