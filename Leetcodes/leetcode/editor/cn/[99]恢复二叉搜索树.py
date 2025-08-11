# 给你二叉搜索树的根节点 root ，该树中的 恰好 两个节点的值被错误地交换。请在不改变其结构的情况下，恢复这棵树 。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [1,3,null,null,2]
# 输出：[3,1,null,null,2]
# 解释：3 不能是 1 的左孩子，因为 3 > 1 。交换 1 和 3 使二叉搜索树有效。
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [3,1,4,null,null,2]
# 输出：[2,1,4,null,null,3]
# 解释：2 不能在 3 的右子树中，因为 2 < 3 。交换 2 和 3 使二叉搜索树有效。 
# 
#  
# 
#  提示： 
# 
#  
#  树上节点的数目在范围 [2, 1000] 内 
#  -2³¹ <= Node.val <= 2³¹ - 1 
#  
# 
#  
# 
#  进阶：使用 O(n) 空间复杂度的解法很容易实现。你能想出一个只使用 O(1) 空间的解决方案吗？ 
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 1008 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def recoverTree_wrong(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        # 定义两个指针，分别指向两个错误的节点
        w1 = TreeNode(float('inf'))
        w2 = TreeNode(float('inf'))
        # 定义一个队列，用于存储节点
        q = [root]
        # why wrong遍历二叉树,只能解决当前层，解决不了后面的层
        while q:
            # 遍历左子树，将节点压入栈中
            node = q.pop(0)
            if node.left:
                q.append(node.left)
                # 若当前节点的值小于 w1，则更新 w1
                if node.val < node.left.val:
                    w1 = node
            # 若当前节点的值大于 w2，则更新 w2
            # 若当前节点有右子树，将右子树压入栈中
            if node.right:
                q.append(node.right)
                if node.val > node.right.val:
                    w2 = node
        # 交换 w1 和 w2 的值
        w1.val, w2.val = w2.val, w1.val

    def recoverTree(self, root: Optional[TreeNode]) -> None:

        self.prev = None
        self.first = None
        self.second = None

        def inorder(node):
            if not node:
                return
            '''
            中序遍历函数inorder：递归进行中序遍历。在遍历过程中，检查当前节点值是否小于前一个节点值。如果是，则记录这两个节点：

            第一个错误节点是第一次出现逆序的前一个节点（self.first = self.prev）。

            第二个错误节点是最后一次出现逆序的当前节点（self.second = node）。

            交换节点值：遍历完成后，交换first和second节点的值，恢复BST的正确结构。
            '''
            inorder(node.left)
            if self.prev and self.prev.val > node.val:
                if not self.first:
                    self.first = self.prev
                self.second = node
            self.prev = node
            inorder(node.right)

        inorder(root)
        # Swap the values of the two nodes
        if self.first and self.second:
            self.first.val, self.second.val = self.second.val, self.first.val
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
# 创建Solution实例
    solution = Solution()
    root = TreeNode(1, TreeNode(3), TreeNode(2))
    print(solution.recoverTree(root))
