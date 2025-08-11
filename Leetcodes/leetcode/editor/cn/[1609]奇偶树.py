# 如果一棵二叉树满足下述几个条件，则可以称为 奇偶树 ： 
# 
#  
#  二叉树根节点所在层下标为 0 ，根的子节点所在层下标为 1 ，根的孙节点所在层下标为 2 ，依此类推。 
#  偶数下标 层上的所有节点的值都是 奇 整数，从左到右按顺序 严格递增 
#  奇数下标 层上的所有节点的值都是 偶 整数，从左到右按顺序 严格递减 
#  
# 
#  给你二叉树的根节点，如果二叉树为 奇偶树 ，则返回 true ，否则返回 false 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [1,10,4,3,null,7,9,12,8,6,null,null,2]
# 输出：true
# 解释：每一层的节点值分别是：
# 0 层：[1]
# 1 层：[10,4]
# 2 层：[3,7,9]
# 3 层：[12,8,6,2]
# 由于 0 层和 2 层上的节点值都是奇数且严格递增，而 1 层和 3 层上的节点值都是偶数且严格递减，因此这是一棵奇偶树。
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：root = [5,4,2,3,3,7]
# 输出：false
# 解释：每一层的节点值分别是：
# 0 层：[5]
# 1 层：[4,2]
# 2 层：[3,3,7]
# 2 层上的节点值不满足严格递增的条件，所以这不是一棵奇偶树。
#  
# 
#  示例 3： 
# 
#  
# 
#  
# 输入：root = [5,9,1,3,5,7]
# 输出：false
# 解释：1 层上的节点值应为偶数。
#  
# 
#  示例 4： 
# 
#  
# 输入：root = [1]
# 输出：true
#  
# 
#  示例 5： 
# 
#  
# 输入：root = [11,8,6,1,3,9,11,30,20,18,16,12,10,4,2,17]
# 输出：true
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数在范围 [1, 10⁵] 内 
#  1 <= Node.val <= 10⁶ 
#  
# 
#  Related Topics 树 广度优先搜索 二叉树 👍 112 👎 0
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
    def isEvenOddTree1(self, root: Optional[TreeNode]) -> bool:
        # 优化方法是在层序里面直接判断
        # 得到层序数组再判断？
        if not root:
            return True
        ans = []
        path = []
        q = deque([root])
        while q:
            size = len(q)
            for _ in range(size):
                node = q.popleft()
                path.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            ans.append(path)
            path = []
        print(ans)
        # 奇数层判断奇数，偶数层判断偶数,严格增减
        for i in range(len(ans)):
            level = ans[i]
            # 检查奇偶性
            if i % 2 == 0:  # 偶数层，所有值应为奇数且严格递增
                for val in level:
                    if val % 2 != 1:
                        return False
                # 检查严格递增
                for j in range(len(level) - 1):
                    if level[j] >= level[j + 1]:
                        return False
            else:  # 奇数层，所有值应为偶数且严格递减
                for val in level:
                    if val % 2 != 0:
                        return False
                # 检查严格递减
                for j in range(len(level) - 1):
                    if level[j] <= level[j + 1]:
                        return False
        return True
    def isEvenOddTree(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        q = deque([root])
        level = 0  # 当前层数，0表示根节点层
        while q:
            size = len(q)
            prev = None  # 用于检查严格递增或递减
            for _ in range(size):
                node = q.popleft()
                # 检查奇偶性
                if level % 2 == 0:  # 偶数层，值应为奇数
                    if node.val % 2 != 1:
                        return False
                else:  # 奇数层，值应为偶数
                    if node.val % 2 != 0:
                        return False
                # 检查严格递增或递减
                if prev is not None:
                    if level % 2 == 0:  # 偶数层，严格递增
                        if node.val <= prev:
                            return False
                    else:  # 奇数层，严格递减
                        if node.val >= prev:
                            return False
                prev = node.val
                # 将子节点加入队列
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            level += 1
        return True

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(1)
    root.left = TreeNode(10)
    root.right = TreeNode(4)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(12)
    root.left.right.left = TreeNode(8)
    root.left.right.right = TreeNode(6)
    root.right.right.left = TreeNode(2)
    root1 = TreeNode(5)
    root1.left = TreeNode(4)
    root1.right = TreeNode(2)
    root1.left.left = TreeNode(3)
    root1.left.right = TreeNode(3)
    root1.right.right = TreeNode(7)
    print(solution.isEvenOddTree(root1))
