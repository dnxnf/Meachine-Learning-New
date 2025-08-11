# 给定一个 N 叉树，返回其节点值的层序遍历。（即从左到右，逐层遍历）。 
# 
#  树的序列化输入是用层序遍历，每组子节点都由 null 值分隔（参见示例）。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [1,null,3,2,4,null,5,6]
# 输出：[[1],[3,2,4],[5,6]]
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,
# null,13,null,null,14]
# 输出：[[1],[2,3,4,5],[6,7,8,9,10],[11,12,13],[14]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  树的高度不会超过 1000 
#  树的节点总数在 [0, 10⁴] 之间 
#  
# 
#  Related Topics 树 广度优先搜索 👍 500 👎 0
from collections import deque
from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
"""
# Definition for a Node.

"""
class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children
class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        if not root:
            return
        q = deque([root])
        res = []
        path = []
        # bfs 层序遍历
        # 对于当前层
        while q:
            cur_lever = len(q)
            for i in range(cur_lever):
                node = q.popleft()
                path.append(node.val)
                if node.children:
                    # 在当前层把下一层的加进去，到了下一次在pop出来
                    # children是一个列表
                    q.extend(node.children)
            res.append(path.copy())
            path.clear()
        return res

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])
    print(solution.levelOrder(root))