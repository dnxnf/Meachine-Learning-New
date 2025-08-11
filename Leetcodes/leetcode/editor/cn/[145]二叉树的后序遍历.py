# 给你一棵二叉树的根节点 root ，返回其节点值的 后序遍历 。 
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：root = [1,null,2,3] 
#  
# 
#  输出：[3,2,1] 
# 
#  解释： 
# 
#  
# 
#  示例 2： 
# 
#  
#  输入：root = [1,2,3,4,5,null,8,null,null,6,7,9] 
#  
# 
#  输出：[4,6,7,5,2,9,8,3,1] 
# 
#  解释： 
# 
#  
# 
#  示例 3： 
# 
#  
#  输入：root = [] 
#  
# 
#  输出：[] 
# 
#  示例 4： 
# 
#  
#  输入：root = [1] 
#  
# 
#  输出：[1] 
# 
#  
# 
#  提示： 
# 
#  
#  树中节点的数目在范围 [0, 100] 内 
#  -100 <= Node.val <= 100 
#  
# 
#  
# 
#  进阶：递归算法很简单，你可以通过迭代算法完成吗？ 
# 
#  Related Topics 栈 树 深度优先搜索 二叉树 👍 1240 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            res.append(node.val)
        dfs(root)
        return res
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)