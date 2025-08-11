# 输入一棵二叉树的根节点，判断该树是不是平衡二叉树。如果某二叉树中任意节点的左右子树的深度相差不超过1，那么它就是一棵平衡二叉树。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：root = [3,9,20,null,null,15,7]
# 输出：true 
# 解释：如下图
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [1,2,2,3,3,null,null,4,4]
# 输出：false
# 解释：如下图
#  
# 
#  
#  
# 
#  提示： 
# 
#  
#  0 <= 树的结点个数 <= 10000 
#  
# 
#  注意：本题与主站 110 题相同：https://leetcode-cn.com/problems/balanced-binary-tree/ 
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 401 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        res = True
        def dfs(node):
            nonlocal res
            if not node:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            if abs(left - right) > 1:
                res = False
            #     返回当前树的的深度
            return max(left, right) + 1

        dfs(root)
        return bool(res)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
