# 有 n 个网络节点，标记为 1 到 n。 
# 
#  给你一个列表 times，表示信号经过 有向 边的传递时间。 times[i] = (ui, vi, wi)，其中 ui 是源节点，vi 是目标节点， 
# wi 是一个信号从源节点传递到目标节点的时间。 
# 
#  现在，从某个节点 K 发出一个信号。需要多久才能使所有节点都收到信号？如果不能使所有节点收到信号，返回 -1 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
# 输出：2
#  
# 
#  示例 2： 
# 
#  
# 输入：times = [[1,2,1]], n = 2, k = 1
# 输出：1
#  
# 
#  示例 3： 
# 
#  
# 输入：times = [[1,2,1]], n = 2, k = 2
# 输出：-1
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= k <= n <= 100 
#  1 <= times.length <= 6000 
#  times[i].length == 3 
#  1 <= ui, vi <= n 
#  ui != vi 
#  0 <= wi <= 100 
#  所有 (ui, vi) 对都 互不相同（即，不含重复边） 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 最短路 堆（优先队列） 👍 867 👎 0
import heapq
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 有向图的最短路径算法,使用Dijkstra算法,spfa，优先队列和普通队列
#  todo 没太学会，之后在回来看看
# 对于找最短路径问题，先初始化一个距离数组，将原点到每个节点的当前距离存进去，逐步更新,最后取这个距离数组的最大值
# 对于每个节点，遍历邻居，如果到邻居的距离小于等于到当前节点的距离加上邻居到当前节点的距离，则更新邻居的距离
# 最后返回距离数组的最大值，如果有inf，则说明不能到达所有节点，返回-1
class Solution:
    def networkDelayTime1(self, times: List[List[int]], n: int, k: int) -> int:
        # note 优先队列，dijkstra算法
        # 构建图的邻接表
        grape = [[] for _ in range(n + 1)]
        for u, v, w in times:
            grape[u].append([v, w])  # 边 u -> v 权重 w
        # visited = [False] * n  # 标记节点是否访问过
        heap = [(0, k)]  # 优先队列，初始节点为 k，距离为 0
        dist = [float('inf')] * (n + 1)  # 记录节点到源点的最短距离
        dist[k] = 0  # 初始节点到源点的距离为 0
        while heap:
            d, u = heapq.heappop(heap)  # 弹出距离最小的节点
            if d > dist[u]: continue  # 距离超过当前最短距离，跳过
            for v, w in grape[u]:  # 遍历 u 的邻接节点
                if dist[u] + w < dist[v]:  # 更新距离
                    dist[v] = dist[u] + w
                    heapq.heappush(heap, (dist[v], v))  # 加入优先队列
        maxn = max(dist[1:])  # 找到最大距离
        return maxn if maxn != float('inf') else -1  # 返回 -1 表示不能到达所有节点

    def networkDelayTime2(self, times: List[List[int]], n: int, k: int) -> int:
        # 普通队列，复杂度为v*e
        # bellman-ford算法,也就是bfs算法，复杂度为v*e,被称为SPFA
        graph = [[] for _ in range(n + 1)]
        for u, v, w in times:
            graph[u].append([v, w])
        #     邻接表和距离数组
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        q = [k]
        while q:
            u = q.pop(0)
            # 遍历所有邻居
            for v, w in graph[u]:
                # 松弛操作：如果找到更短路径
                # 如果到达v的距离小于等于到u的距离加上v到u的距离，则更新v的距离
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    if v not in q:  # 避免重复处理
                        q.append(v)

        maxn = max(dist[1:])
        return maxn if maxn != float('inf') else -1

    def networkDelayTime3(self, times: List[List[int]], n: int, k: int) -> int:
        # 构建邻接表
        graph = [[] for _ in range(n + 1)]
        for u, v, w in times:
            graph[u].append((v, w))

        # 初始化距离数组
        dist = [float('inf')] * (n + 1)
        dist[k] = 0

        # DFS函数

        def dfs(node):
            # 遍历所有邻居
            for neighbor, time in graph[node]:
                # 如果找到更短路径
                if dist[neighbor] > dist[node] + time:
                    dist[neighbor] = dist[node] + time
                    dfs(neighbor)  # 继续深入

        dfs(k)

        max_dist = max(dist[1:])
        return max_dist if max_dist != float('inf') else -1

    def networkDelayTime_floyd_original(self, times: List[List[int]], n: int, k: int) -> int:
        # 应该也能用floyd算法，复杂度为v^3,不过这个是求的所有节点的最短路径，应该只求k就好了
        graph = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            graph[i][i] = 0
        for u, v, w in times:
            graph[u][v] = w

        for i in range(n + 1):
            print(graph[i])

        for t in range(n + 1):
            for i in range(n + 1):
                for j in range(n + 1):
                    if graph[i][t] + graph[t][j] < graph[i][j]:
                        graph[i][j] = graph[i][t] + graph[t][j]
        print('-----------')
        for i in range(n + 1):
            print(graph[i])
        # print("第k行：", graph[k])
        max_dist = max(graph[k][1:])
        # print(max_dist)
        return max_dist if max_dist != float('inf') else -1

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # 只求k到其他节点的路径
        graph = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            graph[i][i] = 0
        for u, v, w in times:
            graph[u][v] = w

        for i in range(n + 1):
            print(graph[i])

        for t in range(n + 1):
            for i in range(n + 1):
                for j in range(n + 1):
                    if graph[i][t] + graph[t][j] < graph[i][j]:
                        graph[i][j] = graph[i][t] + graph[t][j]
        print('-----------')
        for i in range(n + 1):
            print(graph[i])
        # print("第k行：", graph[k])
        max_dist = max(graph[k][1:])
        # print(max_dist)
        return max_dist if max_dist != float('inf') else -1


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.networkDelayTime2([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))
