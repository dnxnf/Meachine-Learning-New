# 实现一个函数，检查一棵二叉树是否为二叉搜索树。 
# 示例 1：
# 
#  
# 输入：
#     2
#    / \
#   1   3
# 输出：true
#  
# 
# 示例 2：
# 
#  
# 输入：
#     5
#    / \
#   1   4
#      / \
#     3   6
# 输出：false
# 解释：输入为: [5,1,4,null,null,3,6]。
#      根节点的值为 5 ，但是其右子节点值为 4 。 
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 110 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # 二叉搜索树，其先序(左中右）遍历得到的序列是递增的
        res = []
        def dfs(node):
            if not node:
                return None
            left = dfs(node.left)
            res.append(node.val)
            right = dfs(node.right)
            return res
        dfs(root)
        if len(res) != len(set(res)):
            return False
        return res == sorted(res)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)