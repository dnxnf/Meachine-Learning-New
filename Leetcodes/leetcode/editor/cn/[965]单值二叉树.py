# 如果二叉树每个节点都具有相同的值，那么该二叉树就是单值二叉树。 
# 
#  只有给定的树是单值二叉树时，才返回 true；否则返回 false。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  输入：[1,1,1,1,1,null,1]
# 输出：true
#  
# 
#  示例 2： 
# 
#  
# 
#  输入：[2,2,2,5,2]
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  给定树的节点数范围是 [1, 100]。 
#  每个节点的值都是整数，范围为 [0, 99] 。 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 212 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isUnivalTree(self, root: Optional[TreeNode]) -> bool:
        #         遍历，值都等于root.val就true，否则false
        flag = 1

        def dfs(node: TreeNode) -> bool:

            nonlocal flag, root
            # 空树
            if not node:
                return True
            # 当前节点与根节点不相等时候
            if node.val != root.val:
                flag = 0
                return bool(flag)
            # 都存在不为空
            dfs(node.left)
            dfs(node.right)
            return bool(flag)
        return dfs(root)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
