# 有一个具有 n 个顶点的 双向 图，其中每个顶点标记从 0 到 n - 1（包含 0 和 n - 1）。图中的边用一个二维整数数组 edges 表示，其中 
# edges[i] = [ui, vi] 表示顶点 ui 和顶点 vi 之间的双向边。 每个顶点对由 最多一条 边连接，并且没有顶点存在与自身相连的边。 
# 
#  请你确定是否存在从顶点 source 开始，到顶点 destination 结束的 有效路径 。 
# 
#  给你数组 edges 和整数 n、source 和 destination，如果从 source 到 destination 存在 有效路径 ，则返回 
# true，否则返回 false 。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
# 输出：true
# 解释：存在由顶点 0 到顶点 2 的路径:
# - 0 → 1 → 2 
# - 0 → 2
#  
# 
#  示例 2： 
#  
#  
# 输入：n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
# 
# 输出：false
# 解释：不存在由顶点 0 到顶点 5 的路径.
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 2 * 10⁵ 
#  0 <= edges.length <= 2 * 10⁵ 
#  edges[i].length == 2 
#  0 <= ui, vi <= n - 1 
#  ui != vi 
#  0 <= source, destination <= n - 1 
#  不存在重复边 
#  不存在指向顶点自身的边 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 图 👍 239 👎 0
from collections import deque
from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
from typing import List


# favour 图中两个顶点是否有路径 并查集 dfs bfs

class Solution:
    def validPath1(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        # 并查集
        if source == destination:
            return True

        # 并查集实现
        parent = [i for i in range(n)]

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]  # 路径压缩
                u = parent[u]
            return u

        def union(u, v):
            root_u = find(u)
            root_v = find(v)
            if root_u != root_v:
                parent[root_v] = root_u

        for u, v in edges:
            union(u, v)

        return find(source) == find(destination)

    def validPath2(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        # dfs
        if source == destination:
            return True
        visited = set()
        # 邻接表是顶点个数
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        def dfs(u, v):  # u->v
            if u == v:
                return True
            visited.add(u)
            for node in graph[u]:
                if node not in visited:
                    if dfs(node, v):
                        return True
            return False

        return dfs(source, destination)

    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        # bfs
        if source == destination:
            return True
        visited = set()
        # 邻接表是顶点个数
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        q = deque([source])
        while q:
            node = q.popleft()
            if node == destination:
                return True
            # favour bfs优化，已经访问过的节点，不用再访问
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    q.append(neighbor)
        return False


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2))
    # print(solution.validPath())
