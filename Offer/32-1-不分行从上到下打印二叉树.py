'''
题目：从上到下打印出二叉树的每个节点，同一层的节点按照从左到右的顺序打印。
'''

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
class Solution:
    def print_from_top_to_bottom(self, root):
        if not root:
            return
        queue = [root]
        path = []
        while queue:
            node = queue.pop(0)
            # print(node.val)
            path.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        print(path)
tree = TreeNode(1)
tree.left = TreeNode(2)
tree.right = TreeNode(3)
tree.left.left = TreeNode(4)
tree.left.right = TreeNode(5)
s = Solution()
s.print_from_top_to_bottom(tree)