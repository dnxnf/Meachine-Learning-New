# 给你一个二叉树的根节点 root ，树中每个节点都存放有一个 0 到 9 之间的数字。
# 
#  
#  
#  每条从根节点到叶节点的路径都代表一个数字： 
#  
#  
# 
#  
#  例如，从根节点到叶节点的路径 1 -> 2 -> 3 表示数字 123 。 
#  
# 
#  计算从根节点到叶节点生成的 所有数字之和 。 
# 
#  叶节点 是指没有子节点的节点。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [1,2,3]
# 输出：25
# 解释：
# 从根到叶子节点路径 1->2 代表数字 12
# 从根到叶子节点路径 1->3 代表数字 13
# 因此，数字总和 = 12 + 13 = 25 
# 
#  示例 2： 
#  
#  
# 输入：root = [4,9,0,5,1]
# 输出：1026
# 解释：
# 从根到叶子节点路径 4->9->5 代表数字 495
# 从根到叶子节点路径 4->9->1 代表数字 491
# 从根到叶子节点路径 4->0 代表数字 40
# 因此，数字总和 = 495 + 491 + 40 = 1026
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点的数目在范围 [1, 1000] 内 
#  0 <= Node.val <= 9 
#  树的深度不超过 10 
#  
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 815 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        # res = []

        def dfs(node, num):
            if not node:
                return 0
            # 得先对上一步的num处理,然后判断，不然先到叶子再加，就加不上了

            num = num * 10 + node.val
            # 到了叶子节点，返回数字
            if not node.left and not node.right:
                return num



            res1 = dfs(node.left, num)
            res2 = dfs(node.right, num)
            return res1 + res2

        return dfs(root, 0)


#             path是存储当前路径的一个列表

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    print(solution.sumNumbers(root))
