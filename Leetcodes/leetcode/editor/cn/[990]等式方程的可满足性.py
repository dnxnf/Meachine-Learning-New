# 给定一个由表示变量之间关系的字符串方程组成的数组，每个字符串方程 equations[i] 的长度为 4，并采用两种不同的形式之一："a==b" 或 "a!
# =b"。在这里，a 和 b 是小写字母（不一定不同），表示单字母变量名。 
# 
#  只有当可以将整数分配给变量名，以便满足所有给定的方程时才返回 true，否则返回 false。 
# 
#  
# 
#  
#  
# 
#  示例 1： 
# 
#  输入：["a==b","b!=a"]
# 输出：false
# 解释：如果我们指定，a = 1 且 b = 1，那么可以满足第一个方程，但无法满足第二个方程。没有办法分配变量同时满足这两个方程。
#  
# 
#  示例 2： 
# 
#  输入：["b==a","a==b"]
# 输出：true
# 解释：我们可以指定 a = 1 且 b = 1 以满足满足这两个方程。
#  
# 
#  示例 3： 
# 
#  输入：["a==b","b==c","a==c"]
# 输出：true
#  
# 
#  示例 4： 
# 
#  输入：["a==b","b!=c","c==a"]
# 输出：false
#  
# 
#  示例 5： 
# 
#  输入：["c==c","b==d","x!=z"]
# 输出：true
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= equations.length <= 500 
#  equations[i].length == 4 
#  equations[i][0] 和 equations[i][3] 是小写字母 
#  equations[i][1] 要么是 '='，要么是 '!' 
#  equations[i][2] 是 '=' 
#  
# 
#  Related Topics 并查集 图 数组 字符串 👍 347 👎 0

from typing import List, Optional


# favour 并查集基础
# leetcode submit region begin(Prohibit modification and deletion)
class UnionFind:
    # 初始化
    def __init__(self, n: int):
        self.fa = [i for i in range(n)]

    # 查找元素根节点
    def find(self, x) -> int:
        while self.fa[x] != x:  # 找到父节点
            self.fa[x] = self.fa[self.fa[x]]  # 路径压缩
            x = self.fa[x]
        #     返回的是根节点
        return x

    # 合并
    def union(self, x, y) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        # 根节点编号相同，则已经属于同一集合，不用合并
        if root_x == root_y:
            return False
        #         编号不同时,没有联通，合并
        self.fa[root_y] = root_x
        return True

    def is_connected(self, x, y) -> bool:
        # 两个的根结点相等则连通，返回True
        return self.find(x) == self.find(y)


class Solution:
    def equationsPossible(self, equ: List[str]) -> bool:
        ufind = UnionFind(26)
        for eq in equ:
            if eq[1] == '=':
                # ord(a) = 97
                idx1 = ord(eq[0]) - 97
                idx2 = ord(eq[3]) - 97
                ufind.union(idx1, idx2)  # 合并
        #         两次循环，先找到所有并集，然后查
        for eq in equ:
            if eq[1] == '!':
                idx1 = ord(eq[0]) - 97
                idx2 = ord(eq[3]) - 97
                # 不相等，但还是能找到，则是有问题
                if ufind.is_connected(idx1, idx2):
                    return False
        return True


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.equationsPossible(["a==b", "b!=c", "c==a"]))
