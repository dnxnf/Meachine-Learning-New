# 请设计一个函数判断一棵二叉树是否 轴对称 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [6,7,7,8,9,9,8]
# 输出：true
# 解释：从图中可看出树是轴对称的。 
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：root = [1,2,2,null,3,null,3]
# 输出：false
# 解释：从图中可看出最后一层的节点不对称。 
# 
#  
# 
#  提示： 
# 
#  0 <= 节点个数 <= 1000 
# 
#  注意：本题与主站 101 题相同：https://leetcode-cn.com/problems/symmetric-tree/ 
# 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 484 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def checkSymmetricTree(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        def dfs(left, right):
            # 左右一个空，一个不空，左右不相等
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False
            res = dfs(left.left, right.right) and dfs(left.right, right.left)
            return res
        return dfs(root.left, root.right)



#             不对称条件，
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
