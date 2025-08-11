# 在二叉树中，根节点位于深度 0 处，每个深度为 k 的节点的子节点位于深度 k+1 处。 
# 
#  如果二叉树的两个节点深度相同，但 父节点不同 ，则它们是一对堂兄弟节点。 
# 
#  我们给出了具有唯一值的二叉树的根节点 root ，以及树中两个不同节点的值 x 和 y 。 
# 
#  只有与值 x 和 y 对应的节点是堂兄弟节点时，才返回 true 。否则，返回 false。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：root = [1,2,3,4], x = 4, y = 3
# 输出：false
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [1,2,3,null,4,null,5], x = 5, y = 4
# 输出：true
#  
# 
#  示例 3： 
# 
#  
# 
#  
# 输入：root = [1,2,3,null,4], x = 2, y = 3
# 输出：false 
# 
#  
# 
#  提示： 
# 
#  
#  二叉树的节点数介于 2 到 100 之间。 
#  每个节点的值都是唯一的、范围为 1 到 100 的整数。 
#  
# 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 360 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# noinspection PyCompatibility,PyUnboundLocalVariable
class Solution:
    def isCousins1(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        #         需要x和y的深度和父节点，如果父节点的深度一样，则true
        x_depth, y_depth = None, None
        x_parent, y_parent = None, None
        x_found, y_found = False, False

        def dfs(node: TreeNode, depth: int, parent: TreeNode):
            if not node:
                return
            # 修改此函数外的变量
            nonlocal x_depth, y_depth, x_parent, y_parent, x_found, y_found
            # 找到目标节点
            if node.val == x:
                x_depth = depth
                x_parent = parent
                x_found = True
            elif node.val == y:
                y_depth = depth
                y_parent = parent
                y_found = True
            # 都找到了,可以提前退出循环,也就是循环退出条件
            if x_found and y_found:
                return
            dfs(node.left, depth + 1, node)
            dfs(node.right, depth + 1, node)

        dfs(root, 0, None)
        return x_depth == y_depth and x_parent != y_parent

    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        #  广度优先搜索
        #  层次遍历，深度相同，但是父亲不同时，认为是同样兄弟节点
        #  记录每一层的节点，以及父亲的值，如果在同一层，并且父亲不一样， 认为是堂兄弟
        if not root:
            return False
        pa1, pa2 = TreeNode(), TreeNode()
        q = [root]
        path = []
        res = []
        while q:
            size = len(q)  # 记录当前层节点数
            for i in range(size):
                node = q.pop(0)
                path.append(node.val)
                # if node.val == x or node.val == y:
                if node.left:
                    q.append(node.left)
                    # path.append(node.left.val)
                    if node.left.val == x:
                        pa1 = node
                    elif node.left.val == y:
                        pa2 = node
                if node.right:
                    q.append(node.right)
                    # path.append(node.right.val)
                    if node.right.val == x:
                        pa1 = node
                    elif node.right.val == y:
                        pa2 = node
            res.append(path.copy())
            path = []
        # print(res) # 打印每一层节点值

        if len(res) < 2:
            return False
        # 找到x和y的父节点
        for i in range(2, len(res)):
            if x in res[i] and y in res[i] and pa1.val != pa2.val:
                return True
        return False


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    print(solution.isCousins(root, 4, 3))
