# 给你二叉树的根节点 root 和一个整数目标和 targetSum ，找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。 
# 
#  叶子节点 是指没有子节点的节点。 
# 
#  
#  
#  
#  
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
# 输出：[[5,4,11,2],[5,8,4,5]]
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [1,2,3], targetSum = 5
# 输出：[]
#  
# 
#  示例 3： 
# 
#  
# 输入：root = [1,2], targetSum = 0
# 输出：[]
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点总数在范围 [0, 5000] 内 
#  -1000 <= Node.val <= 1000 
#  -1000 <= targetSum <= 1000 
#  
# 
#  Related Topics 树 深度优先搜索 回溯 二叉树 👍 1188 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        # dfs 得到路径，然后判断是否等于目标值
        def dfs(node, path, cur):
            if not node:
                return
            path.append(node.val)
            # 当你执行 cur += node.val 时，实际上是创建了一个新的整数对象。
            cur += node.val
            if not node.left and not node.right and cur == targetSum:
                res.append(path.copy())
                # 因为return了，下面的代码不执行了，也得return
                path.pop()
                #
                return
            dfs(node.left, path, cur)
            dfs(node.right, path, cur)
            path.pop()

        res = []
        dfs(root, [], 0)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.right.left = TreeNode(5)
    root.right.right.right = TreeNode(1)
    targetSum = 22
    print(solution.pathSum(root, targetSum))
