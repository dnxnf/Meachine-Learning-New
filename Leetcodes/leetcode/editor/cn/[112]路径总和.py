# 给你二叉树的根节点 root 和一个表示目标和的整数 targetSum 。判断该树中是否存在 根节点到叶子节点 的路径，这条路径上所有节点值相加等于目标和
#  targetSum 。如果存在，返回 true ；否则，返回 false 。 
# 
#  叶子节点 是指没有子节点的节点。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
# 输出：true
# 解释：等于目标和的根节点到叶节点路径如上图所示。
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [1,2,3], targetSum = 5
# 输出：false
# 解释：树中存在两条根节点到叶子节点的路径：
# (1 --> 2): 和为 3
# (1 --> 3): 和为 4
# 不存在 sum = 5 的根节点到叶子节点的路径。 
# 
#  示例 3： 
# 
#  
# 输入：root = [], targetSum = 0
# 输出：false
# 解释：由于树是空的，所以不存在根节点到叶子节点的路径。
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点的数目在范围 [0, 5000] 内 
#  -1000 <= Node.val <= 1000 
#  -1000 <= targetSum <= 1000 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 1454 👎 0
from collections import deque
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def hasPathSum1(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # 和上面没啥大区别，只是把path去掉了
        res = []
        if not root:
            return False

        # 当前节点,剩余目标，路径
        def dfs(node, target, sum):
            if not node:
                return 0
            if not node.left and not node.right:
                sum = sum + node.val
                res.append(sum)
            if node.left:
                dfs(node.left, target - sum, sum + node.val)
            if node.right:
                dfs(node.right, target - sum, sum + node.val)

        dfs(root, targetSum, 0)
        print(res)
        if targetSum in res:
            return True
        return False

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        #         上面都是dfs，这个是bfs
        if not root:
            return False

        a = deque([root.val])
        q = deque([root])
        path = [root.val]
        # q 是变化的当前层节点，
        # 出栈这一下是重点，通过出栈逐个处理同层的节点
        while q:
            # 还有东西的时候先取出来判断，然后再把左右孩子的加进去
            curNode = q.popleft()
            # path.append(curNode.val)
            curSum = a.popleft()
            # 是叶子节点，且路径和等于
            if not curNode.left and not curNode.right:
                if curSum == targetSum:
                    return True
            if curNode.left:
                q.append(curNode.left)
                path.append(curNode.left.val)
                a.append(curSum + curNode.left.val)
            if curNode.right:
                q.append(curNode.right)
                path.append(curNode.right.val)
                a.append(curSum + curNode.right.val)
        return False


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
    root.right.right.right = TreeNode(1)

    print(solution.hasPathSum(root, 22))
