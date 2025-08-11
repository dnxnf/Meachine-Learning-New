# 给定一个二叉树的 根节点 root，请找出该二叉树的 最底层 最左边 节点的值。 
# 
#  假设二叉树中至少有一个节点。 
# 
#  
# 
#  示例 1: 
# 
#  
# 
#  
# 输入: root = [2,1,3]
# 输出: 1
#  
# 
#  示例 2: 
# 
#  
# 
#  
# 输入: [1,2,3,4,null,5,6,null,null,7]
# 输出: 7
#  
# 
#  
# 
#  提示: 
# 
#  
#  二叉树的节点个数的范围是 [1,10⁴] 
#  
#  -2³¹ <= Node.val <= 2³¹ - 1 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 631 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        # 最下层的第一个节点，可以层次遍历，bfs
        res = []
        path = []
        q = [root]
        while q:
            size = len(q)
            for i in range(size):
                node = q.pop(0)
                path.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(path) # 最左边的节点
            path = []
        # path = []
        return res[-1][0]
    # def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
    #     # dfs，
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)