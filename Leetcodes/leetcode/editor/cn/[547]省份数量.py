# 
#  
#  有 n 个城市，其中一些彼此相连，另一些没有相连。如果城市 a 与城市 b 直接相连，且城市 b 与城市 c 直接相连，那么城市 a 与城市 c 间接相连
# 。 
#  
#  
# 
#  省份 是一组直接或间接相连的城市，组内不含其他没有相连的城市。 
# 
#  给你一个 n x n 的矩阵 isConnected ，其中 isConnected[i][j] = 1 表示第 i 个城市和第 j 个城市直接相连，而 
# isConnected[i][j] = 0 表示二者不直接相连。 
# 
#  返回矩阵中 省份 的数量。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：isConnected = [[1,1,0],[1,1,0],[0,0,1]]
# 输出：2
#  
# 
#  示例 2： 
#  
#  
# 输入：isConnected = [[1,0,0],[0,1,0],[0,0,1]]
# 输出：3
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 200 
#  n == isConnected.length 
#  n == isConnected[i].length 
#  isConnected[i][j] 为 1 或 0 
#  isConnected[i][i] == 1 
#  isConnected[i][j] == isConnected[j][i] 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 图 👍 1216 👎 0
from collections import deque
from typing import List, Optional


# favour 图的dfs，bfs，并查集,bfs没有显示的遍历目标，每个都要遍历的写法
# leetcode submit region begin(Prohibit modification and deletion)
class Union:
    def __init__(self, n):
        self.fa = [i for i in range(n)]

    def find(self, x):
        while self.fa[x] != x:
            # 压缩
            self.fa[x] = self.fa[self.fa[x]]
            x = self.fa[x]
        return x

    def union(self, x, y):
        root1 = self.find(x)
        root2 = self.find(y)
        if root1 == root2:
            return False
        self.fa[root1] = root2
        return True

    def is_connected(self, x, y):
        return self.find(x) == self.find(y)


class Solution:
    def findCircleNum1(self, city: List[List[int]]) -> int:
        num = len(city)
        ufind = Union(num)
        #       对于每个城市，如果i，j ==1，则i，j连通，则合并
        for i in range(num):
            # 遍历每个城市,检查是否联通，联通就加到一起
            for j in range(i + 1, num):
                if city[i][j] == 1:  # ij联通
                    ufind.union(i, j)
        res = []
        for i in range(num):
            # 存储每个城市的根节点，再通过set去重
            res.append(ufind.find(i))
        # 排除重复的根结点
        return len(set(res))

    def findCircleNum2(self, isConnected: List[List[int]]) -> int:
        # dfs
        n = len(isConnected)
        visited = [False] * n
        res = 0
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and isConnected[i][j] == 1:
                    graph[i].append(j)
                    graph[j].append(i)  # 可写可不写，因为无向图

        def dfs(i):
            visited[i] = True
            for j in graph[i]:
                if not visited[j]:
                    dfs(j)

        for i in range(n):
            if not visited[i]:
                dfs(i)
                res += 1
        return res

    def findCircleNum3(self, isConnected: List[List[int]]) -> int:
        # bfs
        n = len(isConnected)
        visited = [False] * n
        res = 0
        q = deque()
        # 对于每个节点，都加入队列进行广搜,并且标记访问过的节点
        for i in range(n):
            # 在if里面，只访问没有访问过的节点
            if not visited[i]:
                q.append(i)
                visited[i] = True
                # 取出队首元素，广搜其相邻节点，并标记访问过的节点
                while q:
                    node = q.popleft()
                    for j in range(n):
                        if isConnected[node][j] == 1 and not visited[j]:
                            q.append(j)
                            visited[j] = True
                res += 1
        return res

    def findCircleNum4(self, isConnected: List[List[int]]) -> int:
        # dfs
        # 先构建邻接表
        m, n = len(isConnected), len(isConnected[0])
        graph = [[] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if isConnected[i][j] == 1:
                    graph[i].append(j)
        # 开始dfs
        visited = [False] * n
        res = 0

        def dfs(i):
            visited[i] = True
            for j in graph[i]:
                if not visited[j]:
                    dfs(j)

        for i in range(n):
            if not visited[i]:
                dfs(i)
                res += 1
        return res

    def findCircleNum(self, isConnected: List[List[int]]) -> int:
#         bfs
        n = len(isConnected)
        visited = [False] * n
        res = 0
        q = deque()
        # 对于每个节点，都加入队列进行广搜,并且标记访问过的节点
        for i in range(n):
            if not visited[i]:
                q.append(i)
                visited[i] = True
                while q:
                    node = q.popleft()
                    for j in range(n):
                        if isConnected[node][j] == 1 and not visited[j]:
                            q.append(j)
                            visited[j] = True
                res += 1
        return res

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]))
