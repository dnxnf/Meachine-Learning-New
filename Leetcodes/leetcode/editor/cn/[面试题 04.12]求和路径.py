# 给定一棵二叉树，其中每个节点都含有一个整数数值(该值或正或负)。设计一个算法，打印节点数值总和等于某个给定值的所有路径的数量。注意，路径不一定非得从二叉树的
# 根节点或叶节点开始或结束，但是其方向必须向下(只能从父节点指向子节点方向)。 
# 
#  示例： 给定如下二叉树，以及目标和 sum = 22， 
# 
#  
#               5
#              / \
#             4   8
#            /   / \
#           11  13  4
#          /  \    / \
#         7    2  5   1
#  
# 
#  输出： 
# 
#  
# 3
# 解释：和为 22 的路径有：[5,4,11,2], [5,8,4,5], [4,11,7] 
# 
#  提示： 
# 
#  
#  节点总数 <= 10000 
#  
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 148 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], sum: int) -> int:
        # 定义一个递归函数，传入根节点和目标和,
        res = []

        def dfs(node, target, path):
            # node为当前节点，target为目标和，path为当前路径
            if not node:
                return 0
            new_target = target - node.val
            new_path = path + [node.val]
            if new_target == 0:
                print(new_path)
                res.append(new_path[:])
            dfs(node.left, new_target, new_path)
            dfs(node.right, new_target, new_path)

        def dfs_v2(node):
            # 递归搜索节点
            if not node:
                return 0
            dfs(node, sum, [])
            if node.right:
                dfs_v2(node.right)
            if node.left:
                dfs_v2(node.left)

        dfs_v2(root)
        # 双重递归，一层遍历所有点，一层遍历所有路径
        return len(res)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.pathSum(TreeNode(5, TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))),
                                    TreeNode(8, TreeNode(13), TreeNode(4, None, TreeNode(5, None, TreeNode(1))))), 22))
