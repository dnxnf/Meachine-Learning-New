# 小镇里有 n 个人，按从 1 到 n 的顺序编号。传言称，这些人中有一个暗地里是小镇法官。 
# 
#  如果小镇法官真的存在，那么： 
# 
#  
#  小镇法官不会信任任何人。 
#  每个人（除了小镇法官）都信任这位小镇法官。 
#  只有一个人同时满足属性 1 和属性 2 。 
#  
# 
#  给你一个数组 trust ，其中 trust[i] = [ai, bi] 表示编号为 ai 的人信任编号为 bi 的人。 
# 
#  如果小镇法官存在并且可以确定他的身份，请返回该法官的编号；否则，返回 -1 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 2, trust = [[1,2]]
# 输出：2
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 3, trust = [[1,3],[2,3]]
# 输出：3
#  
# 
#  示例 3： 
# 
#  
# 输入：n = 3, trust = [[1,3],[2,3],[3,1]]
# 输出：-1
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 1000 
#  0 <= trust.length <= 10⁴ 
#  trust[i].length == 2 
#  trust 中的所有trust[i] = [ai, bi] 互不相同 
#  ai != bi 
#  1 <= ai, bi <= n 
#  
# 
#  Related Topics 图 数组 哈希表 👍 384 👎 0

from typing import List, Optional

from typing_extensions import Counter


# leetcode submit region begin(Prohibit modification and deletion)
from typing import List
# what 出度和入度
class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        # 初始化两个数组，分别记录每个人的出度和入度
        out_degrees = [0] * (n + 1)  # out_degrees[i] 表示编号为 i 的人信任了多少人
        in_degrees = [0] * (n + 1)   # in_degrees[i] 表示编号为 i 的人被多少人信任

        # 遍历 trust 列表，更新出度和入度
        for a, b in trust:
            out_degrees[a] += 1
            in_degrees[b] += 1

        # 寻找法官
        for i in range(1, n + 1):
            if out_degrees[i] == 0 and in_degrees[i] == n - 1:
                return i

        return -1


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findJudge(n=2, trust=[[1, 3], [2, 3], [3, 1]]))
