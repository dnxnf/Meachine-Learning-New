# 树可以看成是一个连通且 无环 的 无向 图。 
# 
#  给定往一棵 n 个节点 (节点值 1～n) 的树中添加一条边后的图。添加的边的两个顶点包含在 1 到 n 中间，且这条附加的边不属于树中已存在的边。图的信
# 息记录于长度为 n 的二维数组 edges ，edges[i] = [ai, bi] 表示图中在 ai 和 bi 之间存在一条边。 
# 
#  请找出一条可以删去的边，删除后可使得剩余部分是一个有着 n 个节点的树。如果有多个答案，则返回数组 edges 中最后出现的那个。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入: edges = [[1,2], [1,3], [2,3]]
# 输出: [2,3]
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入: edges = [[1,2], [2,3], [3,4], [1,4], [1,5]]
# 输出: [1,4]
#  
# 
#  
# 
#  提示: 
# 
#  
#  n == edges.length 
#  3 <= n <= 1000 
#  edges[i].length == 2 
#  1 <= ai < bi <= edges.length 
#  ai != bi 
#  edges 中无重复元素 
#  给定的图是连通的 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 图 👍 707 👎 0

from typing import List, Optional

# what 并查集
# leetcode submit region begin(Prohibit modification and deletion)
class UnionFind:
    def __init__(self, n):
        # fa father
        self.fa = [i for i in range(n)]

    def find(self, x):  # 返回根节点序号，不在其他的里面，那就是自己
        while self.fa[x] != x:  # 当前节点不是根节点继续找
            self.fa[x] = self.fa[self.fa[x]]  # 路径压缩,
            x = self.fa[x]
        return x

    def union(self, x, y):
        # 获得根节点
        root1 = self.find(x)
        root2 = self.find(y)
        if root1 == root2:
            return False
        # 右边的赋给左边
        self.fa[root1] = root2
        return True

    def is_connected(self, x, y):
        return self.find(x) == self.find(y)


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # 从1开始，并查集得多一个节点，所以+1
        ufind = UnionFind(len(edges) + 1)
        print(ufind.fa)
        num = len(edges)
        res = []

        for i in range(0, num):
            # 遍历每个城市,检查是否联通，联通就加到一起
            # ufind.union(edges[i][0], edges[i][1])
            x, y = edges[i][0], edges[i][1]
            # ufind.union说明在一起了，not取反说明合并过，冗余了
            if not ufind.union(x, y):
                res = edges[i]
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))
