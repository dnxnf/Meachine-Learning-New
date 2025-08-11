# 小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为
#  root 。 
# 
#  除了
#  root 之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。 如果 两个直接相连的
# 房子在同一天晚上被打劫 ，房屋将自动报警。 
# 
#  给定二叉树的 root 。返回 在不触动警报的情况下 ，小偷能够盗取的最高金额 。 
# 
#  
# 
#  示例 1: 
# 
#  
# 
#  
# 输入: root = [3,2,3,null,3,null,1]
# 输出: 7 
# 解释: 小偷一晚能够盗取的最高金额 3 + 3 + 1 = 7 
# 
#  示例 2: 
# 
#  
# 
#  
# 输入: root = [3,4,5,1,3,null,1]
# 输出: 9
# 解释: 小偷一晚能够盗取的最高金额 4 + 5 = 9
#  
# 
#  
# 
#  提示： 
# 
#  
#  
# 
#  
#  树的节点数在 [1, 10⁴] 范围内 
#  0 <= Node.val <= 10⁴ 
#  
# 
#  Related Topics 树 深度优先搜索 动态规划 二叉树 👍 2099 👎 0
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rob_wrong(self, root: Optional[TreeNode]) -> int:
        # bfs得到层序遍历，将奇偶层的分别求解
        # 只能找到奇偶层的max，不一定是全局的max
        if not root:
            return 0
        queue = [root]
        res = [0, 0]
        flag = 0
        while queue:
            size = len(queue)
            for i in range(size):
                node = queue.pop(0)
                if flag % 2 == 0:
                    res[0] += node.val
                else:
                    res[1] += node.val
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            flag += 1
        return max(res)

    def rob_wrong2(self, root: Optional[TreeNode]) -> int:
        # 动态规划
        # 定义dp[i]为第i层的最大收益
        # 得先获得列表形状的层次遍历，再根据层次遍历计算dp
        lst = []
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
            lst.append(path)
            path = []
        # 计算dp
        print(lst)
        # dp = [0] * (len(lst) + 1)
        # 定义dp[i]为第i层的最大收益
        if len(lst) == 1:
            return lst[0][0]
        if len(lst) == 2:
            return max(sum(lst[1]), lst[0][0])

        dp = [0] * (len(lst))
        dp[0] = sum(lst[0])
        dp[1] = max(sum(lst[1]), dp[0])
        for i in range(2, len(lst)):
            dp[i] = max(dp[i - 1], dp[i - 2] + sum(lst[i]))
        return dp[-1]

    def rob1(self, root: Optional[TreeNode]) -> int:
        # favour dfs的记忆化搜索，后面还有动态规划的 上面两种方法都是只能考虑不相邻层的，
        #  这个可以考虑所有情况，但是需要记忆化搜索，否则hi超时
        if not root:
            return 0

        # dfs, 递归计算子树的最大收益
        # flag = 1  表示选了当前节点，左右孩子不能选，flag = 2 表示没选当前节点，左右孩子可以选
        memo = {}

        def dfs(node, flag):
            global res
            if not node:
                return 0
            if (node, flag) in memo:  # 如果已经计算过，直接返回结果
                return memo[(node, flag)]
            # 当前节点选了，左右孩子不选

            if flag == 1:
                res = node.val + dfs(node.left, 2) + dfs(node.right, 2)
            if flag == 2:
                # note 选左孩子或不选左孩子的最大值，这个很重要，这样写才能考虑所有情况
                #  flag == 2（不选当前节点）时，左右孩子可以选或不选，因此需要比较选和不选左右孩子的最大值。
                left = max(dfs(node.left, 1), dfs(node.left, 2))
                right = max(dfs(node.right, 1), dfs(node.right, 2))
                res = left + right
            memo[(node, flag)] = res
            return res  # 记录结果

        return max(dfs(root, 1), dfs(root, 2))

    def rob3(self, root: Optional[TreeNode]) -> int:
        # 更简单的记忆化搜索,使用lru_cache装饰器
        if not root:
            return 0

        @lru_cache(maxsize=None)
        def dfs(node, flag):
            if not node:
                return 0

            # 当前节点选了，左右孩子不选,
            # flag=1表示当前节点可以选,flag=2表示当前节点不能选
            if flag == 1:
                return node.val + dfs(node.left, 2) + dfs(node.right, 2)
            # 当前节点没选，左右孩子可以选或不选，取最大值
            else:
                # 选左孩子或不选左孩子的最大值
                left = max(dfs(node.left, 1), dfs(node.left, 2))
                # 选右孩子或不选右孩子的最大值
                right = max(dfs(node.right, 1), dfs(node.right, 2))
                return left + right

        return max(dfs(root, 1), dfs(root, 2))

    def rob(self, root: Optional[TreeNode]) -> int:
        # note 树形dp，还是一样的，不要考虑递归过程，直接考虑结果。
        # 结果就是返回了偷或不偷当前节点的最大值。
        # 所以先获得左右子树的最大值，再判断要不要偷当前节点。
        # 因为这样写是正确的，并且考虑到了叶子节点的边界情况，因此子节点也正确，所以可以这样写。
        def dfs(node):
            if not node:
                return (0, 0)  # (rob_current, not_rob_current)
            left = dfs(node.left)
            right = dfs(node.right)
            # 从叶子节点开始计算每个节点的最大收益
            # 选当前节点，则不能选左右孩子
            rob_current = node.val + left[1] + right[1]
            # 不选当前节点，则可以选或不选左右孩子
            not_rob_current = max(left[0], left[1]) + max(right[0], right[1])

            return (rob_current, not_rob_current)

        result = dfs(root)
        return max(result[0], result[1])


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(3)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(3)
    root.right.right = TreeNode(1)
    # root = TreeNode(3)
    print(solution.rob3(root))
