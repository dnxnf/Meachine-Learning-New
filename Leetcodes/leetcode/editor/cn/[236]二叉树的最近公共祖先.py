# 给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。 
# 
#  百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（
# 一个节点也可以是它自己的祖先）。” 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
# 输出：3
# 解释：节点 5 和节点 1 的最近公共祖先是节点 3 。
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
# 输出：5
# 解释：节点 5 和节点 4 的最近公共祖先是节点 5 。因为根据定义最近公共祖先节点可以为节点本身。
#  
# 
#  示例 3： 
# 
#  
# 输入：root = [1,2], p = 1, q = 2
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数目在范围 [2, 10⁵] 内。 
#  -10⁹ <= Node.val <= 10⁹ 
#  所有 Node.val 互不相同 。 
#  p != q 
#  p 和 q 均存在于给定的二叉树中。 
#  
# 
#  Related Topics 树 深度优先搜索 二叉树 👍 2995 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor1(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        #
        if not root:
            return None
        if root == p or root == q:
            return root
#         对于此问题，深搜,递归的是能否在左右子树中找到p和q，如果找到了，就返回当前节点，如果没有找到，就返回None
#         递归的是当前节点的子树有没有p或q，有的话返回，没有就返回空
#         note 从结果考虑，不要从q过程考虑，
#          结果就是当前左右子树能不能找到p,q，返回的就是p或q,
#          如果都找到了，当前的就是
#          相信这个函数能找到p或q,找到了,那结果就是当前的根节点，找到了一边就返回哪一个
#          只需要关心当前节点的逻辑
#          合并结果：根据左右子树的结果，决定当前节点该返回什么。

        left = self.lowestCommonAncestor1(root.left, p, q)
        right = self.lowestCommonAncestor1(root.right, p, q)
        # 如果左右子树都找到了，就返回当前节点，如果没有找到，就返回None
        # 左右都返回了，说明左右就是pq，那么当前节点就公共祖先
        if left and right:
            return root
        # 如果只有左子树返回非空节点，返回左子树的结果（表示p和q都在左子树中）
        if left:
            return left
        # 如果只有右子树返回非空节点，返回右子树的结果（表示p和q都在右子树中）
        if right:
            return right
        return None

    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        def dfs(node: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> Optional['TreeNode']:
            '''
            返回的是p和q的最近公共祖先，如果根是p或q，返回根节点
            如果左右子树都找到了，就返回当前节点，如果没有找到，就返回None
            如果只有左子树返回非空节点，返回左子树的结果（表示p和q都在左子树中）
            如果只有右子树返回非空节点，返回右子树的结果（表示p和q都在右子树中）
            '''
            if not node:
                return None
            if node == p or node == q:
                return node
            left = dfs(node.left, p, q)
            right = dfs(node.right, p, q)
            if left and right:
                return node
            return left or right
            # return None

        return dfs(root, p, q)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)
    p = TreeNode(5)
    q = TreeNode(1)
    print(solution.lowestCommonAncestor(root, p, q))
