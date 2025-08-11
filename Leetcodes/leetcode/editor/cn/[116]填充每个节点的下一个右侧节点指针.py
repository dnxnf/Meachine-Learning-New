# 给定一个 完美二叉树 ，其所有叶子节点都在同一层，每个父节点都有两个子节点。二叉树定义如下： 
# 
#  
# struct Node {
#   int val;
#   Node *left;
#   Node *right;
#   Node *next;
# } 
# 
#  填充它的每个 next 指针，让这个指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针设置为 NULL。 
# 
#  初始状态下，所有 next 指针都被设置为 NULL。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [1,2,3,4,5,6,7]
# 输出：[1,#,2,3,#,4,5,6,7,#]
# 解释：给定二叉树如图 A 所示，你的函数应该填充它的每个 next 指针，以指向其下一个右侧节点，如图 B 所示。序列化的输出按层序遍历排列，同一层节点由 
# next 指针连接，'#' 标志着每一层的结束。
#  
# 
#  
#  
# 
#  示例 2: 
# 
#  
# 输入：root = []
# 输出：[]
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点的数量在
#  [0, 2¹² - 1] 范围内 
#  -1000 <= node.val <= 1000 
#  
# 
#  
# 
#  进阶： 
# 
#  
#  你只能使用常量级额外空间。 
#  使用递归解题也符合要求，本题中递归程序占用的栈空间不算做额外的空间复杂度。 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 链表 二叉树 👍 1193 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
"""
# Definition for a Node.

"""


class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        # 如果是左子树，则next指向右子树
        # 如果是右子树，则指向父节点的next的左子树
        # 没有，就不用管
        def dfs(node):
            if not node:
                return
            # print(node.val)
            # print(node.next.val)
            # 是左子树，则next指向右子树
            if node and node.left:
                node.left.next = node.right
            #     是右子树，则指向父节点的next的左子树
            if node.right and node.next:
                node.right.next = node.next.left

            dfs(node.left)
            dfs(node.right)
        # print(root)
        dfs(root)
        return root


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7)))
    print(solution.connect(root))
