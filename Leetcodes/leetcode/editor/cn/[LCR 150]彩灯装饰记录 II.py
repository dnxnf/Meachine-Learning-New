# 一棵圣诞树记作根节点为 root 的二叉树，节点值为该位置装饰彩灯的颜色编号。请按照从左到右的顺序返回每一层彩灯编号，每一层的结果记录于一行。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [8,17,21,18,null,null,6]
# 输出：[[8],[17,21],[18,6]]
#  
# 
#  提示： 
# 
#  
#  节点总数 <= 1000 
#  
# 
#  注意：本题与主站 102 题相同：https://leetcode-cn.com/problems/binary-tree-level-order-
# traversal/ 
# 
#  
# 
#  Related Topics 树 广度优先搜索 二叉树 👍 323 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def decorateRecord(self, root: Optional[TreeNode]) -> List[List[int]]:
        res = []
        if not root:
            return res
        queue = [root]
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.pop(0)
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            res.append(level)
        return res
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)