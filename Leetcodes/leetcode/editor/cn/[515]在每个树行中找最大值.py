# 给定一棵二叉树的根节点 root ，请找出该二叉树中每一层的最大值。 
# 
#  
# 
#  示例1： 
# 
#  
# 
#  
# 输入: root = [1,3,2,5,3,null,9]
# 输出: [1,3,9]
#  
# 
#  示例2： 
# 
#  
# 输入: root = [1,2,3]
# 输出: [1,3]
#  
# 
#  
# 
#  提示： 
# 
#  
#  二叉树的节点个数的范围是 [0,10⁴] 
#  
#  -2³¹ <= Node.val <= 2³¹ - 1 
#  
# 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 397 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def largestValues(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        res = []
        # path = []
        q = [root]
        while q:
            size = len(q)
            max_val = float('-inf')
            for i in range(size):
                node = q.pop(0)
                max_val = max(max_val, node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(max_val)
        return res
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)