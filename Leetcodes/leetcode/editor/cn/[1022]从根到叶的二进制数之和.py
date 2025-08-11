# 给出一棵二叉树，其上每个结点的值都是 0 或 1 。每一条从根到叶的路径都代表一个从最高有效位开始的二进制数。 
# 
#  
#  例如，如果路径为 0 -> 1 -> 1 -> 0 -> 1，那么它表示二进制数 01101，也就是 13 。 
#  
# 
#  对树上的每一片叶子，我们都要找出从根到该叶子的路径所表示的数字。 
# 
#  返回这些数字之和。题目数据保证答案是一个 32 位 整数。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [1,0,1,0,1,0,1]
# 输出：22
# 解释：(100) + (101) + (110) + (111) = 4 + 5 + 6 + 7 = 22
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [0]
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中的节点数在 [1, 1000] 范围内 
#  Node.val 仅为 0 或 1 
#  
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 261 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumRootToLeaf(self, root: Optional[TreeNode]) -> int:
        res = []
        path = []

        def dfs(root):
            if not root.left and not root.right:  # 节点可能是0
                # path.append(root.val)
                res.append((path + [root.val]).copy())
                return 0
            path.append(root.val)
            if root.left:
                dfs(root.left)
            if root.right:
                dfs(root.right)
            path.pop()

        dfs(root)
        # print()
        print(res)
        ans = 0
        for i in res:
            ans += int(''.join(map(str, i)), 2)
        return ans


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
# 给出一棵二叉树，其上每个结点的值都是 0 或 1 。每一条从根到叶的路径都代表一个从最高有效位开始的二进制数。
#
#
#  例如，如果路径为 0 -> 1 -> 1 -> 0 -> 1，那么它表示二进制数 01101，也就是 13 。
#
#
#  对树上的每一片叶子，我们都要找出从根到该叶子的路径所表示的数字。
#
#  返回这些数字之和。题目数据保证答案是一个 32 位 整数。
#
#
#
#  示例 1：
#
#
# 输入：root = [1,0,1,0,1,0,1]
# 输出：22
# 解释：(100) + (101) + (110) + (111) = 4 + 5 + 6 + 7 = 22
#
#
#  示例 2：
#
#
# 输入：root = [0]
# 输出：0
#
#
#
#
#  提示：
#
#
#  树中的节点数在 [1, 1000] 范围内
#  Node.val 仅为 0 或 1
#
#
#  Related Topics 树 深度优先搜索 二叉树 👍 261 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# favour 带回溯的dfs得到叶子节点
#  是否需要回溯主要取决于我们如何传递和处理路径信息。以下是两种方法的核心区别及其原因：

class Solution:
    def sumRootToLeaf1(self, root: Optional[TreeNode]) -> int:
        res = []
        path = []

        # 存放结果的res，和记录路径的path
        def dfs(root):
            # 这个return有没有都行
            # if not root:
            #     return
            if not root.left and not root.right:  # 节点可能是0
                # path.append(root.val)
                res.append((path + [root.val]).copy())
                return
            path.append(root.val)
            if root.left:
                dfs(root.left)
            if root.right:
                dfs(root.right)
            path.pop()

        dfs(root)

        print(res)
        ans = 0
        for i in res:
            ans += int(''.join(map(str, i)), 2)
        return ans

    def sumRootToLeaf(self, root: Optional[TreeNode]) -> int:
        #         不使用回溯的方法
        res = []

        def dfs(node, path):
            if not node:
                return
            # 如果是叶子节点，将路径添加到路径列表中
            if not node.left and not node.right:
                res.append((path + [node.val]).copy())
                return
            path.append(node.val)
            # 递归处理左右子树
            dfs(node.left, path.copy())
            dfs(node.right, path.copy())

        dfs(root, [])
        print(res)
        ans = 0
        for i in res:
            ans += int(''.join(map(str, i)), 2)
        return ans


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(1)
    root.left = TreeNode(0)
    root.right = TreeNode(1)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(1)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(1)
    # root = TreeNode()
    print(solution.sumRootToLeaf(root))
