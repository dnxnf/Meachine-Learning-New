# 给你一个二叉树的根节点 root ，按 任意顺序 ，返回所有从根节点到叶子节点的路径。 
# 
#  叶子节点 是指没有子节点的节点。 
# 
#  示例 1： 
#  
#  
# 输入：root = [1,2,3,null,5]
# 输出：["1->2->5","1->3"]
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [1]
# 输出：["1"]
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点的数目在范围 [1, 100] 内 
#  -100 <= Node.val <= 100 
#  
# 
#  Related Topics 树 深度优先搜索 字符串 回溯 二叉树 👍 1230 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def binaryTreePaths1(self, root: Optional[TreeNode]) -> List[str]:
        if not root:
            return []
        elif not root.left and not root.right:
            return [str(root.val)]
        # 有左有右的时候
        else:
            # 左等于左子树，右等于右子树
            left = self.binaryTreePaths(root.left)
            light = self.binaryTreePaths(root.right)
            res = []
            res.extend([str(root.val) + "->" + i for i in left])
            res.extend([str(root.val) + "->" + i for i in light])
            return res

    def binaryTreePaths(self, root: TreeNode) -> List[str]:
        def dfs(node, path):
            # path 是存储节点值的列表
            # 递归结束条件
            if not node.left and not node.right:  # 叶子节点
                res.append('->'.join(path))
                return
            if node.left:  # 有左子树时候
                dfs(node.left, path + [str(node.left.val)])
            if node.right:
                dfs(node.right, path + [str(node.right.val)])

        res = []
        dfs(root, [str(root.val)])
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.binaryTreePaths(1, 2, 3, None, 5))
