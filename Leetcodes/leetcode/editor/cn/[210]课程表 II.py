# 现在你总共有 numCourses 门课需要选，记为 0 到 numCourses - 1。给你一个数组 prerequisites ，其中 
# prerequisites[i] = [ai, bi] ，表示在选修课程 ai 前 必须 先选修 bi 。 
# 
#  
#  例如，想要学习课程 0 ，你需要先完成课程 1 ，我们用一个匹配来表示：[0,1] 。 
#  
# 
#  返回你为了学完所有课程所安排的学习顺序。可能会有多个正确的顺序，你只要返回 任意一种 就可以了。如果不可能完成所有课程，返回 一个空数组 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：numCourses = 2, prerequisites = [[1,0]]
# 输出：[0,1]
# 解释：总共有 2 门课程。要学习课程 1，你需要先完成课程 0。因此，正确的课程顺序为 [0,1] 。
#  
# 
#  示例 2： 
# 
#  
# 输入：numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
# 输出：[0,2,1,3]
# 解释：总共有 4 门课程。要学习课程 3，你应该先完成课程 1 和课程 2。并且课程 1 和课程 2 都应该排在课程 0 之后。
# 因此，一个正确的课程顺序是 [0,1,2,3] 。另一个正确的排序是 [0,2,1,3] 。 
# 
#  示例 3： 
# 
#  
# 输入：numCourses = 1, prerequisites = []
# 输出：[0]
#  
# 
#  
# 提示：
# 
#  
#  1 <= numCourses <= 2000 
#  0 <= prerequisites.length <= numCourses * (numCourses - 1) 
#  prerequisites[i].length == 2 
#  0 <= ai, bi < numCourses 
#  ai != bi 
#  所有[ai, bi] 互不相同 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 拓扑排序 👍 1035 👎 0

from typing import List, Optional

# favour 图的经典拓扑排序
'''
拓扑排序是针对有向无环图（DAG）的线性排序算法，满足：
依赖关系：对于图中的每条有向边 u→v，u 在排序中总是位于 v 的前面
无环约束：只有无环有向图才能进行拓扑排序
通俗理解：就像课程安排，必须先学完基础课才能学进阶课，拓扑排序就是找到一个合理的学习顺序。
'''


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findOrder1(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = [[] for _ in range(numCourses)]
        for course, pre in prerequisites:
            graph[pre].append(course)

        # 状态：0=未访问，1=访问中，2=已完成
        visited = [0] * numCourses
        result = []
        self.cycle_found = False

        def dfs(node):
            # 没找到环
            if self.cycle_found:
                return
            # 环检测，当遇到1状态的节点时，说明存在环,设置cycle_found标志提前终止搜索
            # 因为正常来说都变成2了，如果还是1，说明又走回去了，即有环
            if visited[node] == 1:  # 发现环
                self.cycle_found = True
                return
            # 该节点遍历过
            if visited[node] == 2:  # 已完成的节点
                return

            visited[node] = 1  # 标记为访问中
            # 遍历该节点可以到达的每个节点
            for neighbor in graph[node]:
                dfs(neighbor)

            visited[node] = 2  # 标记为已完成
            result.append(node)  # 后序位置添加节点

        # 遍历所有课程
        for course in range(numCourses):
            # 处理非联通图或者没有出度的节点
            if visited[course] == 0:
                dfs(course)
            if self.cycle_found:
                return []
        # 最先被标记为"已完成"的是最深层的节点（即没有后继的课程）
        # DFS判断有环：会在递归路径中重复访问到状态为"访问中"（标记为1）的节点
        return result[::-1]  # 反转后序结果得到拓扑序

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = [[] for _ in range(numCourses)]
        in_degree = [0] * numCourses
        for course, pre in prerequisites:
            graph[pre].append(course)  # 注意方向：pre → course
            in_degree[course] += 1  # course 的入度 +1
        # Kahn算法
        # 1. 找到入度为0的节点，加入队列
        # 2. 出队一个节点，将其所有出边的入度减1，如果入度变为0，加入队列
        # 3. 重复2，直到队列为空或者有环
        queue = [i for i in range(numCourses) if in_degree[i] == 0]
        result = []
        while queue:
            course = queue.pop(0)
            result.append(course)
            for neighbor in graph[course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return result if len(result) == numCourses else []


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))
