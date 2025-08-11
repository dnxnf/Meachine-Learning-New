# 给定一个 N 叉树，找到其最大深度。 
# 
#  最大深度是指从根节点到最远叶子节点的最长路径上的节点总数。 
# 
#  N 叉树输入按层序遍历序列化表示，每组子节点由空值分隔（请参见示例）。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：root = [1,null,3,2,4,null,5,6]
# 输出：3
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,
# null,13,null,null,14]
# 输出：5
#  
# 
#  
# 
#  提示： 
# 
#  
#  树的深度不会超过 1000 。 
#  树的节点数目位于 [0, 10⁴] 之间。 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 👍 406 👎 0

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
    def maxDepth1(self, root: 'Node') -> int:
        # dfs
        if not root:
            return 0
        if not root.children:
            return 1
        tmax = 0
        for child in root.children:
            tmax = max(tmax, self.maxDepth1(child))
        return tmax + 1

    def maxDepth(self, root: 'Node') -> int:
        #         bfs
        if not root:
            return 0
        res = []
        path = []
        q = [root]
        while q:
            cur = len(q)
            for i in range(cur):
                node = q.pop(0)
                path.append(node)
                if node.children:
                    q.extend(node.children)
            res.append(path.copy())
            path.clear()
        return len(res)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
