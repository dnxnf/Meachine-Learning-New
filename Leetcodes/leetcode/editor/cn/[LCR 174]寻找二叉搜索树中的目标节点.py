# 某公司组织架构以二叉搜索树形式记录，节点值为处于该职位的员工编号。请返回第 cnt 大的员工编号。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [7, 3, 9, 1, 5], cnt = 2
#        7
#       / \
#      3   9
#     / \
#    1   5
# 输出：7
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入: root = [10, 5, 15, 2, 7, null, 20, 1, null, 6, 8], cnt = 4
#        10
#       / \
#      5   15
#     / \    \
#    2   7    20
#   /   / \ 
#  1   6   8
# 输出: 8 
# 
#  
# 
#  提示： 
# 
#  
#  1 ≤ cnt ≤ 二叉搜索树元素个数 
#  
# 
#  
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 423 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def findTargetNode(self, root: Optional[TreeNode], cnt: int) -> int:
#         中序遍历，找到第cnt个节点
        res = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
        dfs(root)
        return res[len(res) - cnt]
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)