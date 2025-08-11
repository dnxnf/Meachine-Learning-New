# 你这个学期必须选修 numCourses 门课程，记为 0 到 numCourses - 1 。 
# 
#  在选修某些课程之前需要一些先修课程。 先修课程按数组 prerequisites 给出，其中 prerequisites[i] = [ai, bi] ，表
# 示如果要学习课程 ai 则 必须 先学习课程 bi 。 
# 
#  
#  例如，先修课程对 [0, 1] 表示：想要学习课程 0 ，你需要先完成课程 1 。 
#  
# 
#  请你判断是否可能完成所有课程的学习？如果可以，返回 true ；否则，返回 false 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：numCourses = 2, prerequisites = [[1,0]]
# 输出：true
# 解释：总共有 2 门课程。学习课程 1 之前，你需要完成课程 0 。这是可能的。 
# 
#  示例 2： 
# 
#  
# 输入：numCourses = 2, prerequisites = [[1,0],[0,1]]
# 输出：false
# 解释：总共有 2 门课程。学习课程 1 之前，你需要先完成​课程 0 ；并且学习课程 0 之前，你还应先完成课程 1 。这是不可能的。 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= numCourses <= 2000 
#  0 <= prerequisites.length <= 5000 
#  prerequisites[i].length == 2 
#  0 <= ai, bi < numCourses 
#  prerequisites[i] 中的所有课程对 互不相同 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 拓扑排序 👍 2165 👎 0
from collections import deque
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 拓扑排序，判断有向图是否有环，kahn算法，还有构建邻接表
class Solution:
    def canFinish1(self, numCs: int, preReq: List[List[int]]) -> bool:
        # 相当于一个有向图，不构成环即可。
        # 构建邻接表
        graph = [[] for _ in range(numCs)]
        for src, dst in preReq:
            # 第一个是先修课程，第二个是要修的课程
            graph[src].append(dst)
        print(graph)
        # 判断是否有环
        visited = [0] * numCs
        '''
        递归返回的是有环还是没环，如果这个节点看到过了，则有环，如果没看到过，则没环
        对每个节点，先弄成1，再查看临接节点，若是临接节点有环，则返回有环，
        否则将这个节点弄成2，返回没环
        '''

        # @lru_cache(None)
        def hasCycle(node):
            # 这个递归思路
            # 判断条件：有环没环,返回的也是true和false
            # 状态：从当前节点到可到达的其他节点看有没有环
            if 1 == visited[node]:
                return True  # 有环
            if 2 == visited[node]:
                return False  # 没有环
            # 这时还是0，先置为1
            visited[node] = 1
            # 对于这个节点能到的其他节点，如果有环，就返回True
            for n in graph[node]:
                if hasCycle(n):
                    return True
            # 其他节点也没环，就返回false
            visited[node] = 2
            return False

        for i in range(numCs):
            if hasCycle(i):
                return False
        return True

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 构建邻接表
        graph = [[] for _ in range(numCourses)]
        # graph 记录的是当前课程的先修课程,解包操作，直接对应元素
        for src, dst in prerequisites:
            graph[dst].append(src)
        print(graph)
        '''
        统计入度，将入度为0的作为开始节点，进行拓扑排序
        维护一个入度为0的队列S，再从队列中取出一个顶点u，加入到order中
        删除这个点，并删除所有以u为起点的边，将所有入度减1
        重复以上步骤，直到队列为空
        '''
        indegrees = [0] * numCourses
        # 第一个节点是后修课程，是有入度的
        for dst in prerequisites:
            indegrees[dst[0]] += 1
        print(indegrees)
        #      入度为0的节点加进来
        q = deque([i for i in range(numCourses) if indegrees[i] == 0])
        print(q)

        if not q:
            return False
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in graph[u]:
                # 先修课程的入度减1
                indegrees[v] -= 1
                # 如果入度为0，就加进来
                if indegrees[v] == 0:
                    q.append(v)
        # 如果order的长度等于numCourses，说明所有课程都可以修完
        # 否则，说明有环
        return len(order) == numCourses


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()

    # print(solution.canFinish1(2, [[1, 0]]))
    print(solution.canFinish(2, [[1, 0], [0, 1]]))
