# 给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。 
# 
#  百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（
# 一个节点也可以是它自己的祖先）。” 
# 
#  例如，给定如下二叉搜索树: root = [6,2,8,0,4,7,9,null,null,3,5] 
# 
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
# 输出：6 
# 解释：节点 2 和节点 8 的最近公共祖先是 6。
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
# 输出：2
# 解释：节点 2 和节点 4 的最近公共祖先是 2, 因为根据定义最近公共祖先节点可以为节点本身。 
# 
#  
# 
#  说明： 
# 
#  
#  所有节点的值都是唯一的。 
#  p、q 为不同节点且均存在于给定的二叉搜索树中。 
#  
# 
#  注意：本题与主站 235 题相同：https://leetcode-cn.com/problems/lowest-common-ancestor-of-
# a-binary-search-tree/ 
# 
#  Related Topics 树 深度优先搜索 二叉搜索树 二叉树 👍 349 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
# favour 二叉树递归，思路很本质，就是找到两个节点的最大公共祖先
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return None
        # 这个点大，说明在左子树
        if root.val > p.val and root.val > q.val:
            return self.lowestCommonAncestor(root.left, p, q)
        # 小，说明你在右子树
        elif root.val < p.val and root.val < q.val:
            return self.lowestCommonAncestor(root.right, p, q)
        else:
            return root
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)