# 给你一棵 完整二叉树 的根，这棵树有以下特征：
#
#
#  叶子节点 要么值为 0 要么值为 1 ，其中 0 表示 False ，1 表示 True 。
#  非叶子节点 要么值为 2 要么值为 3 ，其中 2 表示逻辑或 OR ，3 表示逻辑与 AND 。
#
#
#  计算 一个节点的值方式如下：
#
#
#  如果节点是个叶子节点，那么节点的 值 为它本身，即 True 或者 False 。
#  否则，计算 两个孩子的节点值，然后将该节点的运算符对两个孩子值进行 运算 。
#
#
#  返回根节点 root 的布尔运算值。
#
#  完整二叉树 是每个节点有 0 个或者 2 个孩子的二叉树。
#
#  叶子节点 是没有孩子的节点。
#
#
#
#  示例 1：
#
#
#
#  输入：root = [2,1,3,null,null,0,1]
# 输出：true
# 解释：上图展示了计算过程。
# AND 与运算节点的值为 False AND True = False 。
# OR 运算节点的值为 True OR False = True 。
# 根节点的值为 True ，所以我们返回 true 。
#
#  示例 2：
#
#  输入：root = [0]
# 输出：false
# 解释：根节点是叶子节点，且值为 false，所以我们返回 false 。
#
#
#
#
#  提示：
#
#
#  树中节点数目在 [1, 1000] 之间。
#  0 <= Node.val <= 3
#  每个节点的孩子数为 0 或 2 。
#  叶子节点的值为 0 或 1 。
#  非叶子节点的值为 2 或 3 。
#
#
#  Related Topics 树 深度优先搜索 二叉树 👍 108 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def evaluateTree(self, root: Optional[TreeNode]) -> bool:
        if not root.left and not root.right:
            return bool(root.val)
        res = []
        # 2 表示或，3表示与
        def dfs(node):
            if not node.left and not node.right:
                return bool(node.val)
            left = dfs(node.left)
            right = dfs(node.right)
            if node.val == 2:
                return (left or right)
            elif node.val == 3:
                return (left and right)
            # else:
            #     res.append(bool(node.val))

        return dfs(root)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(1)
    root = TreeNode(0)
    print(solution.evaluateTree(root))