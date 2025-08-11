# 有两个水壶，容量分别为 x 和 y 升。水的供应是无限的。确定是否有可能使用这两个壶准确得到 target 升。 
# 
#  你可以： 
# 
#  
#  装满任意一个水壶 
#  清空任意一个水壶 
#  将水从一个水壶倒入另一个水壶，直到接水壶已满，或倒水壶已空。 
#  
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: x = 3,y = 5,target = 4
# 输出: true
# 解释：
# 按照以下步骤操作，以达到总共 4 升水：
# 1. 装满 5 升的水壶(0, 5)。
# 2. 把 5 升的水壶倒进 3 升的水壶，留下 2 升(3, 2)。
# 3. 倒空 3 升的水壶(0, 2)。
# 4. 把 2 升水从 5 升的水壶转移到 3 升的水壶(2, 0)。
# 5. 再次加满 5 升的水壶(2, 5)。
# 6. 从 5 升的水壶向 3 升的水壶倒水直到 3 升的水壶倒满。5 升的水壶里留下了 4 升水(3, 4)。
# 7. 倒空 3 升的水壶。现在，5 升的水壶里正好有 4 升水(0, 4)。
# 参考：来自著名的 "Die Hard" 
# 
#  示例 2: 
# 
#  
# 输入: x = 2, y = 6, target = 5
# 输出: false
#  
# 
#  示例 3: 
# 
#  
# 输入: x = 1, y = 2, target = 3
# 输出: true
# 解释：同时倒满两个水壶。现在两个水壶中水的总量等于 3。 
# 
#  
# 
#  提示: 
# 
#  
#  1 <= x, y, target <= 10³ 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 数学 👍 554 👎 0
from math import gcd
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def canMeasureWater1(self, x: int, y: int, target: int) -> bool:
        # 可以量出水的条件：
        # 1.target ≤ x + y（因为两个壶的总容量是上限）
        # 2.target % gcd(x, y) == 0（target 必须是 x 和 y 的最大公约数（GCD）的倍数）
        if target == 0:
            return True
        if target > x + y:
            return False

        # 计算x和y的最大公约数
        return target % gcd(x, y) == 0

    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        # dfs 完全没看懂
        if target == 0:
            return True
        if target > x + y:
            return False
        s = [(0, 0)]
        visited = set()
        # 记录当前状态
        visited.add((0, 0))
        while s:
            a, b = s.pop()
            if a == target or b == target or a + b == target:
                return True
            # 生成所有可能的状态
            next = set()
            # 向左倒水
            next.add((x, b))
            # 向右倒水
            next.add((a, y))
            # 倒空a
            next.add((0, b))
            # 倒空b
            next.add((a, 0))
            # 将x倒入y，直到x空或y满

            tep1 = min(a, y - b)
            next.add((a - tep1, b + tep1))
            # 将y倒入x，直到y空或x满
            tep2 = min(b, x - a)
            next.add((a + tep2, b - tep2))
            # 遍历所有可能的状态
            for i, j in next:
                if (i, j) not in visited:
                    visited.add((i, j))
                    s.append((i, j))
        return False


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.canMeasureWater(3, 5, 4))
    print(gcd(2, 6))