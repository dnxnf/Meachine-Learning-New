# 树是一个无向图，其中任何两个顶点只通过一条路径连接。 换句话说，任何一个没有简单环路的连通图都是一棵树。 
# 
#  给你一棵包含 n 个节点的树，标记为 0 到 n - 1 。给定数字 n 和一个有 n - 1 条无向边的 edges 列表（每一个边都是一对标签），其中
#  edges[i] = [ai, bi] 表示树中节点 ai 和 bi 之间存在一条无向边。 
# 
#  可选择树中任何一个节点作为根。当选择节点 x 作为根节点时，设结果树的高度为 h 。在所有可能的树中，具有最小高度的树（即，min(h)）被称为 最小高度
# 树 。 
# 
#  请你找到所有的 最小高度树 并按 任意顺序 返回它们的根节点标签列表。 树的 
# 高度 是指根节点和叶子节点之间最长向下路径上边的数量。
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：n = 4, edges = [[1,0],[1,2],[1,3]]
# 输出：[1]
# 解释：如图所示，当根是标签为 1 的节点时，树的高度是 1 ，这是唯一的最小高度树。 
# 
#  示例 2： 
#  
#  
# 输入：n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
# 输出：[3,4]
#  
# 
#  
# 
#  
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 2 * 10⁴ 
#  edges.length == n - 1 
#  0 <= ai, bi < n 
#  ai != bi 
#  所有 (ai, bi) 互不相同 
#  给定的输入 保证 是一棵树，并且 不会有重复的边 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 拓扑排序 👍 977 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        # 找接的节点最多的节点，其构成的子树很可能是最小高度树
        # fixme 没太看懂，待后续复习
        # favour 无向图的节点构建邻接表,拓扑排序
        #  1. 找出度为1的节点，作为初始的叶子节点
        #  2. 开始拓扑排序，每次删除度为1的节点，并将其邻接节点加入到结果中
        #  3. 重复2，直到所有节点都被删除，剩下的节点即为最小高度树的根节点
        #  4. 返回结果
        if n == 1:
            return [0]

            # 构建邻接表表示的图结构
            # graph[i] 存储与节点i直接相连的所有邻居节点
        graph = [[] for _ in range(n)]
        for src, dst in edges:
            # 无向图需要双向记录边关系
            graph[src].append(dst)
            graph[dst].append(src)

        # 初始化第一层叶子节点（度为1的节点）
        # 这些是最外层的节点，从它们开始向内"剥洋葱"
        leaves = [i for i in range(n) if len(graph[i]) == 1]

        # 记录剩余节点数量，用于控制循环终止
        remaining_nodes = n

        # 拓扑排序核心过程：不断去除叶子节点层，中心节点最多有两个
        # 当剩余节点数大于2时继续（因为中心最多2个节点）
        while remaining_nodes > 2:
            # 更新剩余节点数（减去当前层的叶子节点数）
            remaining_nodes -= len(leaves)
            new_leaves = []  # 准备存储下一层的叶子节点

            # 处理当前层的所有叶子节点
            for leaf in leaves:
                # 获取该叶子节点的唯一邻居（因为度=1）
                neighbor = graph[leaf][0]

                # 双向移除连接关系（从邻居的连接中移除该叶子节点）
                graph[neighbor].remove(leaf)

                # 检查邻居节点是否成为新的叶子节点（度降为1）
                if len(graph[neighbor]) == 1:
                    new_leaves.append(neighbor)

            # 更新叶子节点列表为下一层要处理的节点
            leaves = new_leaves

        # 循环结束时，剩下的节点就是最小高度树的根
        # 可能是1个或2个节点（取决于树的最长路径的奇偶性）
        return leaves


# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()

    print(solution.findMinHeightTrees(4, [[1, 0], [1, 2], [1, 3]]))
