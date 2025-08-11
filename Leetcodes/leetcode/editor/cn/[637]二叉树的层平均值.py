# 给定一个非空二叉树的根节点
#  root , 以数组的形式返回每一层节点的平均值。与实际答案相差 10⁻⁵ 以内的答案可以被接受。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [3,9,20,null,null,15,7]
# 输出：[3.00000,14.50000,11.00000]
# 解释：第 0 层的平均值为 3,第 1 层的平均值为 14.5,第 2 层的平均值为 11 。
# 因此返回 [3, 14.5, 11] 。
#  
# 
#  示例 2: 
# 
#  
# 
#  
# 输入：root = [3,9,20,15,7]
# 输出：[3.00000,14.50000,11.00000]
#  
# 
#  
# 
#  提示： 
# 
#  
#  
# 
#  
#  树中节点数量在 [1, 10⁴] 范围内 
#  -2³¹ <= Node.val <= 2³¹ - 1 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 535 👎 0
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
    def averageOfLevels1(self, root: Optional[TreeNode]) -> List[float]:
        # bfs
        res = []
        path = []
        q = deque([root])
        while q:
            level = len(q)
            for _ in range(level):
                node = q.popleft()
                path.append(node)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(sum(node.val for node in path) / len(path))
            path = []
        return res

    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        # dfs
        res = []
        def dfs(node,depth):
            if not node:
                return
            # 用层次来决定要进入的列表层次
            if len(res) < depth:
                # 添加空列表存储当前层
                res.append([])
            res[depth-1].append(node.val)
            dfs(node.left, depth+1)
            dfs(node.right, depth+1)
        dfs(root, 1)
        return [sum(level) / len(level) for level in res]

# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
