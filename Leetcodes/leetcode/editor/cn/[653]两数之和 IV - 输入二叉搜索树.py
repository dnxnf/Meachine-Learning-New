# 给定一个二叉搜索树 root 和一个目标结果 k，如果二叉搜索树中存在两个元素且它们的和等于给定的目标结果，则返回 true。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入: root = [5,3,6,2,4,null,7], k = 9
# 输出: true
#  
# 
#  示例 2： 
#  
#  
# 输入: root = [5,3,6,2,4,null,7], k = 28
# 输出: false
#  
# 
#  
# 
#  提示: 
# 
#  
#  二叉树的节点个数的范围是 [1, 10⁴]. 
#  -10⁴ <= Node.val <= 10⁴ 
#  题目数据保证，输入的 root 是一棵 有效 的二叉搜索树 
#  -10⁵ <= k <= 10⁵ 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉搜索树 哈希表 双指针 二叉树 👍 522 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        # 二叉搜索树，左小右大，中序遍历得到数组再双指针
        path = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            path.append(node.val)
            dfs(node.right)
        dfs(root)
        i, j = 0, len(path) - 1
        while i < j:
            if path[i] + path[j] == k:
                return True
            elif path[i] + path[j] < k:
                i += 1
            else:
                j -= 1
        return False
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(5, TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(4)), TreeNode(6, None, TreeNode(7)))
    print(solution.findTarget(root, 9))