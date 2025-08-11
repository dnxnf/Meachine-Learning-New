# 给你两棵二叉树的根节点 p 和 q ，编写一个函数来检验这两棵树是否相同。 
# 
#  如果两个树在结构上相同，并且节点具有相同的值，则认为它们是相同的。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：p = [1,2,3], q = [1,2,3]
# 输出：true
#  
# 
#  示例 2： 
#  
#  
# 输入：p = [1,2], q = [1,null,2]
# 输出：false
#  
# 
#  示例 3： 
#  
#  
# 输入：p = [1,2,1], q = [1,1,2]
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  两棵树上的节点数目都在范围 [0, 100] 内 
#  -10⁴ <= Node.val <= 10⁴ 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 1236 👎 0
from collections import deque
from typing import List, Optional


#
# from python.modules import TreeNode


# import TreeNode


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSameTree1(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # 左右都为空
        if not p and not q:
            return True
        # 左右有一个为空
        elif not p or not q:
            return False
        # 左右都不为空，但根值不同,传入的就是根值
        elif p.val != q.val:
            return False
        # 都有值
        else:
            # 左子树相等且右子树相等
            return (self.isSameTree1(p.left, q.left) and
                    self.isSameTree1(p.right, q.right))

    def isSameTree2(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # 三个递归结束条件
        if not p and not q:
            return True
        elif not p or not q:
            return False
        elif p.val != q.val:
            return False
        rot1 = self.isSameTree2(p.left, q.left)
        rot2 = self.isSameTree2(p.right, q.right)
        return rot1 and rot2

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # 广搜，把列表跑出来，挨个对比，
        # 或者同时广搜，看相等不,那么while的条件是q1和q2都不为空
        if not p and not q:
            return True
        elif not p or not q:
            return False
        q1, q2 = deque([p]), deque([q])
#         如果层次遍历，空的也得加进去，否则比不了，同时看两个一样不一样，一样就继续
        while q1 and q2:
            cur1 = len(q1)
            cur2 = len(q2)
            if cur1 != cur2:
                return False
            # cur = cur1
            for i in range(cur1):
                node1 = q1.popleft()
                node2 = q2.popleft()
                if node1.val != node2.val:
                    return False
        #         没必要path和res，直接过程中判断就好了
                if node1.left:
                    if node2.left:
                        q1.append(node1.left)
                        q2.append(node2.left)
                    else:
                        return False
                if node1.right:
                    if node2.right:
                        q1.append(node1.right)
                        q2.append(node2.right)
                    else:
                        return False
                if not node1.left and node2.left:
                    return False
                if not node1.right and node2.right:
                    return False

        #         如果都遍历完了，说明相等
        #     不管空不空，都得加进去

        return True




# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.isSameTree())
