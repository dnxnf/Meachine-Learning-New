# 给你一个二叉树的根节点 root ，判断其是否是一个有效的二叉搜索树。 
# 
#  有效 二叉搜索树定义如下： 
# 
#  
#  节点的左子树只包含 小于 当前节点的数。 
#  节点的右子树只包含 大于 当前节点的数。 
#  所有左子树和右子树自身必须也是二叉搜索树。 
#  
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [2,1,3]
# 输出：true
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [5,1,4,null,null,3,6]
# 输出：false
# 解释：根节点的值是 5 ，但是右子节点的值是 4 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数目范围在[1, 10⁴] 内 
#  -2³¹ <= Node.val <= 2³¹ - 1 
#  
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 2586 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST1(self, root: Optional[TreeNode]) -> bool:
        # 左小右大
        res = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            res.append(node.val)
            inorder(node.right)

        inorder(root)
        for i in range(1, len(res)):
            if res[i] <= res[i - 1]:
                return False
        return True

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # 不使用中序遍历，使用递归
        def dfs(node, lower=float('-inf'), upper=float('inf')):
            # 两个递归结束条件
            if not node:
                return True
            if node.val <= lower or node.val >= upper:
                return False
            left = dfs(node.left, lower, node.val)
            right = dfs(node.right, node.val, upper)
            return left and right

        return dfs(root)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
