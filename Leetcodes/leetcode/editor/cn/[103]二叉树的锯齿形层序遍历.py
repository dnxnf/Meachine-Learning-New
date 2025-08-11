# 给你二叉树的根节点 root ，返回其节点值的 锯齿形层序遍历 。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [3,9,20,null,null,15,7]
# 输出：[[3],[20,9],[15,7]]
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [1]
# 输出：[[1]]
#  
# 
#  示例 3： 
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
#  树中节点数目在范围 [0, 2000] 内 
#  -100 <= Node.val <= 100 
#  
# 
#  Related Topics 树 广度优先搜索 二叉树 👍 966 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        lst = []
        def level(node: TreeNode, depth: int):
            # nonlocal lst
            if not node:
                return
            # 到了下一层
            if len(lst) < depth:
                lst.append([])
            #     奇偶对应不同的插入方法
            if depth % 2 == 1:
                lst[depth - 1].append(node.val)
            #     偶数时，加在最前面
            else:
                lst[depth - 1].insert(0, node.val)
            if node.left:
                level(node.left, depth + 1)
            if node.right:
                level(node.right, depth + 1)
        level(root, 1)
        return lst



# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)