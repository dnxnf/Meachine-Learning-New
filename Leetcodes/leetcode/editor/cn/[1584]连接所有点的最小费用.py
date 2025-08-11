# 给你一个points 数组，表示 2D 平面上的一些点，其中 points[i] = [xi, yi] 。 
# 
#  连接点 [xi, yi] 和点 [xj, yj] 的费用为它们之间的 曼哈顿距离 ：|xi - xj| + |yi - yj| ，其中 |val| 表示 
# val 的绝对值。 
# 
#  请你返回将所有点连接的最小总费用。只有任意两点之间 有且仅有 一条简单路径时，才认为所有点都已连接。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
# 输出：20
# 解释：
# 
# 我们可以按照上图所示连接所有点得到最小总费用，总费用为 20 。
# 注意到任意两个点之间只有唯一一条路径互相到达。
#  
# 
#  示例 2： 
# 
#  
# 输入：points = [[3,12],[-2,5],[-4,1]]
# 输出：18
#  
# 
#  示例 3： 
# 
#  
# 输入：points = [[0,0],[1,1],[1,0],[-1,1]]
# 输出：4
#  
# 
#  示例 4： 
# 
#  
# 输入：points = [[-1000000,-1000000],[1000000,1000000]]
# 输出：4000000
#  
# 
#  示例 5： 
# 
#  
# 输入：points = [[0,0]]
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= points.length <= 1000 
#  -10⁶ <= xi, yi <= 10⁶ 
#  所有点 (xi, yi) 两两不同。 
#  
# 
#  Related Topics 并查集 图 数组 最小生成树 👍 347 👎 0
from math import sqrt
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 最小生成树，权值矩阵,并查集的kruskal算法(没写）
class Solution:
    def getDist1(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        # Output Limit Exceeded
        n = len(points)
        # 建立一个矩阵，存放的是两点之间的距离
        dist = [[0] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
            for j in range(i + 1, n):
                dist[i][j] = self.getDist1(points[i], points[j])
                dist[j][i] = dist[i][j]
        # for i in range(n):
        #     for j in range(i + 1, n):
        #         dist[i][j] = self.getDist1(points[i], points[j])
        #         dist[j][i] = dist[i][j]
        # for i in range(n):
        #     print(dist[i])
        # 得到权值矩阵，现在是每行选一个，让最后的结果最小
        # 最小生成树，Prim算法
        # 先选第一个点，然后选第二个点，第三个点，依次类推，直到选完所有点
        # 选完之后，再选一条最短的边，然后再选第二条最短的边，依次类推，直到所有边都被选过
        # 最后，选完所有边，得到最小生成树
        # 时间复杂度O(n^2),代码如下：

        # Prim算法
        mst = [False] * n  # 记录顶点是否在MST中
        parent = [-1] * n  # 记录MST中顶点的父节点
        key = [float('inf')] * n  # 记录顶点到MST的最小距离

        key[0] = 0  # 从第一个顶点开始

        for _ in range(n):
            # 找到key值最小的未选顶点
            # 临时变量min_key记录最小值，u记录最小值的索引
            u = -1
            min_key = float('inf')
            for v in range(n):
                if not mst[v] and key[v] < min_key:
                    min_key = key[v]
                    u = v

            mst[u] = True

            # 更新相邻顶点的key值
            for v in range(n):
                if not mst[v] and dist[u][v] < key[v]:
                    key[v] = dist[u][v]
                    parent[v] = u

        # 计算总费用
        total_cost = 0
        for i in range(1, n):
            total_cost += dist[parent[i]][i]
        print(parent)
        return total_cost

    def minCostConnectPoints1(self, points: List[List[int]]) -> int:
        n = len(points)
        graph = [[0] * n for _ in range(n)]
        if n <= 1:
            return 0
        # 得到权重矩阵
        for i in range(n):
            for j in range(n):
                if i == j:
                    graph[i][j] = 0
                else:
                    graph[i][j] = self.getDist1(points[i], points[j])
                    graph[j][i] = graph[i][j]

        def prim(start, graph):
            visited = [False] * n  # 记录顶点是否访问过
            dist = [float('inf')] * n  # start到其他点的距离
            size = len(graph)  # 图的大小
            ans = 0  # 最小生成树的总权重
            dist[start] = 0  # start到自身的距离为0
            visited[start] = True
            # 初始化start到其他点的距离
            for i in range(1, size):
                dist[i] = graph[start][i]

            # 开始Prim算法
            while sum(visited) < size:
                # 找到距离最小的未访问顶点
                min_dist = float('inf')
                min_index = -1
                for i in range(size):
                    if not visited[i] and dist[i] < min_dist:
                        min_dist = dist[i]
                        min_index = i
                # 访问该顶点
                visited[min_index] = True
                ans += min_dist
                # 更新距离
                for i in range(size):
                    if not visited[i] and graph[min_index][i] < dist[i]:
                        dist[i] = graph[min_index][i]

            return ans

        res = prim(0, graph)
        return res

    def minCostConnectPoints2(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        # Prim算法优化版（使用优先队列）
        import heapq

        # 计算曼哈顿距离的函数
        def manhattan(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        # 初始化
        visited = [False] * n
        heap = []
        total_cost = 0

        # 从第一个点开始
        # 堆会根据distance（距离）值进行排序，因为它是元组的第一个元素
        heapq.heappush(heap, (0, 0))  # (distance, point_index)

        while heap and sum(visited) < n:
            cost, u = heapq.heappop(heap)
            if visited[u]:
                continue
            visited[u] = True
            total_cost += cost

            # 添加所有未访问邻居到堆中
            for v in range(n):
                if not visited[v]:
                    distance = manhattan(points[u], points[v])
                    heapq.heappush(heap, (distance, v))

        return total_cost


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.minCostConnectPoints2([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))
    print(solution.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))
# learn prim算法