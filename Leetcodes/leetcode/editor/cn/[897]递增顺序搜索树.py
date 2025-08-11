# 给你一棵二叉搜索树的
#  root ，请你 按中序遍历 将其重新排列为一棵递增顺序搜索树，使树中最左边的节点成为树的根节点，并且每个节点没有左子节点，只有一个右子节点。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [5,3,6,2,4,null,8,1,null,null,null,7,9]
# 输出：[1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [5,1,7]
# 输出：[1,null,5,null,7]
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数的取值范围是 [1, 100] 
#  0 <= Node.val <= 1000 
#  
# 
#  Related Topics 栈 树 深度优先搜索 二叉搜索树 二叉树 👍 358 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def increasingBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        path = []

        def dfs(node):
            if not node:
                # path.append(None)
                return
            dfs(node.left)
            path.append(node.val)
            dfs(node.right)
        dfs(root)
        # what 构建新树，要一个根节点，一个辅助节点
        dummy = TreeNode(-1)
        current = dummy
        for val in path:
            current.right = TreeNode(val)
            current = current.right

        return dummy.right
        # 这里的path是中序遍历的结果


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(8)
    root.left.left.left = TreeNode(1)
    root.right.right.left = TreeNode(7)
    root.right.right.right = TreeNode(9)
    print(solution.increasingBST(root))
