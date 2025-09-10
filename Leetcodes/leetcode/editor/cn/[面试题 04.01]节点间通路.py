# 节点间通路。给定有向图，设计一个算法，找出两个节点之间是否存在一条路径。 
# 
#  示例 1： 
# 
#  
#  输入：n = 3, graph = [[0, 1], [0, 2], [1, 2], [1, 2]], start = 0, target = 2
#  输出：true
#  
# 
#  示例 2： 
# 
#  
#  输入：n = 5, graph = [[0, 1], [0, 2], [0, 4], [0, 4], [0, 1], [1, 3], [1, 4], [1
# , 3], [2, 3], [3, 4]], start = 0, target = 4
#  输出：true
#  
# 
#  提示： 
# 
#  
#  节点数量n在[0, 1e5]范围内。 
#  节点编号大于等于 0 小于 n。 
#  图中可能存在自环和平行边。 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 👍 98 👎 0
from collections import deque
from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findWhetherExistsPath(self, n: int, graph: List[List[int]], start: int, target: int) -> bool:
        # 构建邻接表
        adj = [[] for _ in range(n)]
        for u, v in graph:
            adj[u].append(v)
            # adj[v].append(u)
        print(adj)
        visited = set()
        queue = deque()
        queue.append(start)
        visited.add(start)
        while queue:
            node = queue.popleft()
            if node == target:
                return True
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findWhetherExistsPath(3, [[0, 1], [0, 2], [1, 2], [1, 2]], 0, 2))