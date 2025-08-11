# 给定二叉树的根节点 root ，返回所有左叶子之和。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入: root = [3,9,20,null,null,15,7] 
# 输出: 24 
# 解释: 在这个二叉树中，有两个左叶子，分别是 9 和 15，所以返回 24
#  
# 
#  示例 2: 
# 
#  
# 输入: root = [1]
# 输出: 0
#  
# 
#  
# 
#  提示: 
# 
#  
#  节点数在 [1, 1000] 范围内 
#  -1000 <= Node.val <= 1000 
#  
# 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 772 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def sumOfLeftLeaves1(self, root: Optional[TreeNode]) -> int:
        sum = 0
        if not root:
            return sum
        # 是左叶子
        if root.left and not root.left.left and not root.left.right:
            sum += root.left.val
        #    递归
        sum += self.sumOfLeftLeaves1(root.left)
        sum += self.sumOfLeftLeaves1(root.right)
        return sum
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
#         每个节点的左边，遇到了就sum+
        if not root:
            return 0
        # if
        res = 0
        q = [root]
        while q:
            # curl = len(q)
            node = q.pop(0)
            if node.left:
                if not node.left.left and not node.left.right:
                    res += node.left.val
                else:
                    q.append(node.left)
            if node.right:
                q.append(node.right)
        return res

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)