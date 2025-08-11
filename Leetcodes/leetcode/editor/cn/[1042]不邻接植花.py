from collections import deque
# 有 n 个花园，按从 1 到 n 标记。另有数组 paths ，其中 paths[i] = [xi, yi] 描述了花园 xi 到花园 yi 的双向路径。在
# 每个花园中，你打算种下四种花之一。 
# 
#  另外，所有花园 最多 有 3 条路径可以进入或离开. 
# 
#  你需要为每个花园选择一种花，使得通过路径相连的任何两个花园中的花的种类互不相同。 
# 
#  以数组形式返回 任一 可行的方案作为答案 answer，其中 answer[i] 为在第 (i+1) 个花园中种植的花的种类。花的种类用 1、2、3、4 
# 表示。保证存在答案。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 3, paths = [[1,2],[2,3],[3,1]]
# 输出：[1,2,3]
# 解释：
# 花园 1 和 2 花的种类不同。
# 花园 2 和 3 花的种类不同。
# 花园 3 和 1 花的种类不同。
# 因此，[1,2,3] 是一个满足题意的答案。其他满足题意的答案有 [1,2,4]、[1,4,2] 和 [3,2,1]
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 4, paths = [[1,2],[3,4]]
# 输出：[1,2,1,2]
#  
# 
#  示例 3： 
# 
#  
# 输入：n = 4, paths = [[1,2],[2,3],[3,4],[4,1],[1,3],[2,4]]
# 输出：[1,2,3,4]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 10⁴ 
#  0 <= paths.length <= 2 * 10⁴ 
#  paths[i].length == 2 
#  1 <= xi, yi <= n 
#  xi != yi 
#  每个花园 最多 有 3 条路径可以进入或离开 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 👍 245 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
#  favour todo bfs,dfs 贪心，相邻不同色问题
class Solution:
    def gardenNoAdj1(self, num: int, paths: List[List[int]]) -> List[int]:
        # bfs
        graph = [[] for _ in range(num + 1)]
        for path in paths:
            graph[path[0]].append(path[1])
            graph[path[1]].append(path[0])
        res = [0] * (num + 1)
        visited = set()  # 记录已经访问过的花园
        q = deque()
        # i是花园编号
        for i in range(1, num + 1):
            if i not in visited:
                q.append(i)
                visited.add(i)
                res[i] = 1
            while q:
                node = q.popleft()
                for nei in graph[node]:
                    if nei not in visited:
                        visited.add(nei)
                        q.append(nei)
                        # 记录种植过的花的编号
                        used = {res[i] for i in graph[nei] if res[i] != 0}
                        print('used: ', used)
                        # 在1到4中选择第一个未被使用的颜色
                        for color in [1, 2, 3, 4]:
                            if color not in used:
                                res[nei] = color
                                break
        return res[1:]

    def gardenNoAdj2(self, n: int, paths: List[List[int]]) -> List[int]:
        # 构建邻接表，花园编号是1-based
        graph = [[] for _ in range(n + 1)]
        for x, y in paths:
            graph[x].append(y)
            graph[y].append(x)

        res = [0] * (n + 1)  # res[1..n] 存储结果

        for i in range(1, n + 1):
            # 查看当前花园的邻居已经使用的颜色
            # 当前节点的临接节点中，已经被使用的颜色，因为最多三条路径才能这么写
            # 如果一个节点可以连很多，那条件又变了，就得获得每个邻居的颜色，然后选择未使用的颜色
            used_colors = {res[nei] for nei in graph[i] if res[nei] != 0}
            # 在1-4中选择未使用的颜色
            for color in range(1, 5):
                if color not in used_colors:
                    res[i] = color
                    break
        return res[1:]

    def gardenNoAdj(self, n: int, paths: List[List[int]]) -> List[int]:
        #         dfs
        graph = [[] for _ in range(n + 1)]
        for x, y in paths:
            graph[x].append(y)
            graph[y].append(x)
        res = [0] * (n + 1)

        # visited = set()  # 记录已经访问过的花园

        def dfs(node):
            used = {res[nei] for nei in graph[node] if res[nei] != 0}
            for color in range(1, 5):
                if color not in used:
                    res[node] = color
                    break
            for nei in graph[node]:
                if res[nei] == 0:
                    dfs(nei)

        for i in range(1, n + 1):
            if res[i] == 0:
                dfs(i)
        return res[1:]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()

    print(solution.gardenNoAdj1(3, [[1, 2], [2, 3], [3, 1]]))
