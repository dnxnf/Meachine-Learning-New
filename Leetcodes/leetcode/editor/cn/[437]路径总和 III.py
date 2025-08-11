# 给定一个二叉树的根节点 root ，和一个整数 targetSum ，求该二叉树里节点值之和等于 targetSum 的 路径 的数目。 
# 
#  路径 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
# 输出：3
# 解释：和等于 8 的路径有 3 条，如图所示。
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
# 输出：3
#  
# 
#  
# 
#  提示: 
# 
#  
#  二叉树的节点个数的范围是 [0,1000] 
#  
#  -10⁹ <= Node.val <= 10⁹ 
#  -1000 <= targetSum <= 1000 
#  
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 2090 👎 0
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum1(self, root: Optional[TreeNode], targetSum: int) -> int:


        # 递归函数,cur是当前路径和，没必要在叶子节点结束，所以只需要判断是否到达叶子节点即可
        # 返回的是当前根能到达的路径和，所以就是先得到子路径的路径和，再加上当前节点的值
        # 然后判断是否等于targetSum，如果等于，则cnt加1
        self.cnt = 0
        def dfs(node, current_sum):
            if not node:
                return

            # 当前节点加入路径和
            current_sum[0] += node.val

            # 判断是否满足条件
            if current_sum[0] == targetSum:
                self.cnt += 1

            # 递归处理左右子树
            dfs(node.left, current_sum)
            dfs(node.right, current_sum)

            # 回溯，撤销当前节点的值
            current_sum[0] -= node.val

        # 对每个节点进行DFS
        def traverse(node):
            if not node:
                return
            dfs(node, [0])  # 使用列表传递可变对象
            traverse(node.left)
            traverse(node.right)

        traverse(root)
        return self.cnt

    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        self.total = 0

        @lru_cache(maxsize=None)
        def dfs(node, current_sum):
            if not node:
                return 0

            new_sum = current_sum + node.val
            cnt = 1 if new_sum == targetSum else 0
            cnt += dfs(node.left, new_sum)
            cnt += dfs(node.right, new_sum)
            return cnt

        def traverse(node):
            if not node:
                return 0
            return dfs(node, 0) + traverse(node.left) + traverse(node.right)

        return traverse(root)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.pathSum(TreeNode(10, TreeNode(5, TreeNode(3), TreeNode(-3)), TreeNode(3, TreeNode(2), TreeNode(11))), 8))
