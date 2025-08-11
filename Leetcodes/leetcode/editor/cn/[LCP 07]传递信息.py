# 小朋友 A 在和 ta 的小伙伴们玩传信息游戏，游戏规则如下： 
# 
#  
#  有 n 名玩家，所有玩家编号分别为 0 ～ n-1，其中小朋友 A 的编号为 0 
#  每个玩家都有固定的若干个可传信息的其他玩家（也可能没有）。传信息的关系是单向的（比如 A 可以向 B 传信息，但 B 不能向 A 传信息）。 
#  每轮信息必须需要传递给另一个人，且信息可重复经过同一个人 
#  
# 
#  给定总玩家数 n，以及按 [玩家编号,对应可传递玩家编号] 关系组成的二维数组 relation。返回信息从小 A (编号 0 ) 经过 k 轮传递到编号
# 为 n-1 的小伙伴处的方案数；若不能到达，返回 0。 
# 
#  示例 1： 
# 
#  
#  输入：n = 5, relation = [[0,2],[2,1],[3,4],[2,3],[1,4],[2,0],[0,4]], k = 3 
#  
# 
#  输出：3 
# 
#  解释：信息从小 A 编号 0 处开始，经 3 轮传递，到达编号 4。共有 3 种方案，分别是 0->2->0->4， 0->2->1->4， 0->2->
# 3->4。 
# 
#  示例 2： 
# 
#  
#  输入：n = 3, relation = [[0,2],[2,1]], k = 2 
#  
# 
#  输出：0 
# 
#  解释：信息不能从小 A 处经过 2 轮传递到编号 2 
# 
#  限制： 
# 
#  
#  2 <= n <= 10 
#  1 <= k <= 5 
#  1 <= relation.length <= 90, 且 relation[i].length == 2 
#  0 <= relation[i][0],relation[i][1] < n 且 relation[i][0] != relation[i][1] 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 动态规划 👍 297 👎 0
from collections import deque
from typing import List, Optional


# favour 图dfs,也可以动态规划
# leetcode submit region begin(Prohibit modification and deletion)


class Solution:
    # def __init__(self):
    #     self.res = None

    def numWays(self, n: int, rela: List[List[int]], k: int) -> int:
        # favour 通过列表构建图的临接表
        graph = [[] for _ in range(n)]
        for src, dst in rela:
            # src可以给dst传消息,src是索引，邻接表的内容只有可传递的对象
            graph[src].append(dst)

        res = 0
        # 到达第k轮时候，检查当前玩家是不是n-1（即目标玩家），是则res+1
        # 递归先考到达目标的情况，然后相信子问题可以解决就好了
        def dfs(cur, stp):
            # 简单变量要么self，要么nonlocal声明
            nonlocal res
            if stp == k:  # 轮次到k时
                # n是目标玩家，cur是当前玩家，每次加一
                if cur == n - 1:
                    res += 1
                return
            for neighbor in graph[cur]:
                dfs(neighbor, stp + 1)

        # 从玩家0开始DFS搜索，初始轮数为0
        dfs(0, 0)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
