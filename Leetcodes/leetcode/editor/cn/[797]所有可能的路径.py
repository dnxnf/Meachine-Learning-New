# 给你一个有 n 个节点的 有向无环图（DAG），请你找出所有从节点 0 到节点 n-1 的路径并输出（不要求按特定顺序） 
# 
#  
#  graph[i] 是一个从节点 i 可以访问的所有节点的列表（即从节点 i 到节点 graph[i][j]存在一条有向边）。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：graph = [[1,2],[3],[3],[]]
# 输出：[[0,1,3],[0,2,3]]
# 解释：有两条路径 0 -> 1 -> 3 和 0 -> 2 -> 3
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：graph = [[4,3,1],[3,2,4],[3],[4],[]]
# 输出：[[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  n == graph.length 
#  2 <= n <= 15 
#  0 <= graph[i][j] < n 
#  graph[i][j] != i（即不存在自环） 
#  graph[i] 中的所有元素 互不相同 
#  保证输入为 有向无环图（DAG） 
#  
# 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 回溯 👍 536 👎 0
from collections import deque
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def allPathsSourceTarget1(self, graph: List[List[int]]) -> List[List[int]]:
        # bfs
        res = []
        # 初始化一个双端队列，其中包含一个列表元素 [0]
        q = deque([[0]])
        n = len(graph)
        while q:
            path = q.popleft()
            if path[-1] == n - 1:
                res.append(path)
                continue
            #     当前路径最后一个节点的所有邻居
            for next in graph[path[-1]]:
                q.append(path + [next])
        return res

    def allPathsSourceTarget2(self, graph: List[List[int]]) -> List[List[int]]:
        #       dfs
        n = len(graph)

        # 深搜
        def dfs(node):
            if node == n - 1:
                return [[n - 1]]
            ans = []
            # 对于序号为node的节点，找出他的下一个
            for next in graph[node]:
                for i in dfs(next):
                    ans.append([node] + i)
            return ans

        return dfs(0)

    def allPathsSourceTarget3(self, graph: List[List[int]]) -> List[List[int]]:
        # 带回溯的dfs,需要一个path记录路径，一个res统一所有路径
        # 因为是有向无环图，所以不用visited
        n = len(graph)  # 图中节点的数量
        result = []  # 存储所有从源到目标的路径

        def dfs(cur, path):
            # 将当前节点加入路径
            path.append(cur)

            # 如果当前节点是目标节点，则将路径加入结果
            if cur == n - 1:
                result.append(path.copy())  # 注意要复制路径
            else:
                # 否则，递归访问所有邻居节点
                for neighbor in graph[cur]:
                    dfs(neighbor, path)

            # 回溯，移除当前节点，以便访问其他路径
            path.pop()

        # 初始化路径，从节点 0 开始
        dfs(0, [])
        return result

    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        # 适应了有环图，若有环图使用上述方法会导致无线递归，
        # 所以需要一个visited集合，记录已访问的节点，避免重复访问
        n = len(graph)  # 图中节点的数量
        result = []  # 存储所有从源到目标的路径

        def dfs(current_node, path, visited):
            # 将当前节点加入路径
            path.append(current_node)
            visited.add(current_node)  # 标记当前节点为已访问

            # 如果当前节点是目标节点，则将路径加入结果
            if current_node == n - 1:
                result.append(path.copy())  # 注意要复制路径，避免后续修改影响结果
            else:
                # 否则，递归访问所有邻居节点
                for neighbor in graph[current_node]:
                    if neighbor not in visited:  # 额外判断，避免重复访问
                        dfs(neighbor, path, visited)

            # 回溯，移除当前节点，以便访问其他路径
            path.pop()
            visited.remove(current_node)  # 取消标记

        # 初始化路径和访问集合，从节点 0 开始
        dfs(0, [], set())
        return result

# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.allPathsSourceTarget([[1, 2], [3], [3], []]))
