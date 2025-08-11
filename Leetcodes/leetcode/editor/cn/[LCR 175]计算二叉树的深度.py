# 某公司架构以二叉树形式记录，请返回该公司的层级数。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [1, 2, 2, 3, null, null, 5, 4, null, null, 4]
# 输出: 4
# 解释: 上面示例中的二叉树的最大深度是 4，沿着路径 1 -> 2 -> 3 -> 4 或 1 -> 2 -> 5 -> 4 到达叶节点的最长路径上有 4 
# 个节点。
#  
# 
#  
# 
#  提示： 
# 
#  
#  节点总数 <= 10000 
#  
# 
#  注意：本题与主站 104 题相同：https://leetcode-cn.com/problems/maximum-depth-of-binary-
# tree/ 
# 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 277 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def calculateDepth(self, root: Optional[TreeNode]) -> int:
        # depth = 0
        def dfs(node):
            if not node:
                return 0
            tep1, tep2 = 0, 0
            if node.left:
                tep1 = dfs(node.left)
            if node.right:
                tep2 = dfs(node.right)
            return max(tep1, tep2) + 1

        return dfs(root)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
