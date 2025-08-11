# 给你一个二叉树的根节点 root ， 检查它是否轴对称。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [1,2,2,3,4,4,3]
# 输出：true
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [1,2,2,null,3,null,3]
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数目在范围 [1, 1000] 内 
#  -100 <= Node.val <= 100 
#  
# 
#  
# 
#  进阶：你可以运用递归和迭代两种方法解决这个问题吗？ 
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 2960 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSymmetric1(self, root: Optional[TreeNode]) -> bool:
        # root2 = root
        if not root:
            return True

        # 判断左右子树是否对称
        def dfs(left, right):
            # 先写递归条件,三个
            # 左右都不为空
            # 左右一个空，一个不空
            # 左右不相等
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False
            # 剩下的是左右子树都存在且相等的情况
            return (dfs(left.left, right.right)
                    and dfs(left.right, right.left))

        return dfs(root.left, root.right)

    def isSymmetric2(self, root: Optional[TreeNode]) -> bool:
        # if not root:
        #     return True
        # note 对于递归，先写递归条件，再写当前层逻辑，最后写递归调用
        def dfs(left, right):
            # 能走到叶子，则最后一次判断
            # 没左或没右
            # 左右值不相等
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False
            rot1 = dfs(left.left, right.right)
            rot2 = dfs(left.right, right.left)
            return rot1 and rot2

        return dfs(root.left, root.right)

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        #         自己手写版
        # if not root:
        #     return True
        # if not root.left and not root.right:
        #     return True

        #         深搜，逐渐比较
        def dfs(left, right):
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False
            tep1 = dfs(left.left, right.right)
            tep2 = dfs(left.right, right.left)
            return tep1 and tep2

        return dfs(root.left, root.right)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
