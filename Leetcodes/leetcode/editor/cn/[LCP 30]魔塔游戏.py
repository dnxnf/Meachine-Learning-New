# 小扣当前位于魔塔游戏第一层，共有 `N` 个房间，编号为 `0 ~ N-1`。每个房间的补血道具/怪物对于血量影响记于数组 `nums`，其中正数表示道具补
# 血数值，即血量增加对应数值；负数表示怪物造成伤害值，即血量减少对应数值；`0` 表示房间对血量无影响。
# 
# **小扣初始血量为 1，且无上限**。假定小扣原计划按房间编号升序访问所有房间补血/打怪，**为保证血量始终为正值**，小扣需对房间访问顺序进行调整，**每
# 次仅能将一个怪物房间（负数的房间）调整至访问顺序末尾**。请返回小扣最少需要调整几次，才能顺利访问所有房间。若调整顺序也无法访问完全部房间，请返回 -1。
# 
# **示例 1：**
# 
# > 输入：`nums = [100,100,100,-250,-60,-140,-50,-50,100,150]`
# >
# > 输出：`1`
# >
# > 解释：初始血量为 1。至少需要将 nums[3] 调整至访问顺序末尾以满足要求。
# 
# **示例 2：**
# 
# > 输入：`nums = [-200,-300,400,0]`
# >
# > 输出：`-1`
# >
# > 解释：调整访问顺序也无法完成全部房间的访问。
# 
# **提示：**
# - `1 <= nums.length <= 10^5`
# - `-10^5 <= nums[i] <= 10^5`
# 
#  Related Topics 贪心 数组 堆（优先队列） 👍 126 👎 0
import heapq
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def magicTower(self, nums: List[int]) -> int:
        # 判断总血量是否足够
        if sum(nums) + 1 <= 0:
            return -1

        cur_hp = 1  # 当前血量
        hp_heap = []  # 小顶堆，存负数（伤害值）
        cnt = 0  # 调整次数

        for num in nums:
            cur_hp += num  # 先吃/打这个房间
            if num < 0:
                heapq.heappush(hp_heap, num)  # 记录这个怪物

            # 如果当前血量 <= 0，必须移走一个怪物（伤害最大的）
            while cur_hp <= 0 and hp_heap:
                # 弹出伤害最大的怪物（堆顶，最小的负数）
                max_damage = heapq.heappop(hp_heap)
                cur_hp -= max_damage  # 把扣的血加回来（因为移走了）
                cnt += 1

            # 如果血量 <=0 且没有怪物可移了 → 不可能了（理论上不会发生，因为前面判断了总和）
            if cur_hp <= 0:
                return -1

        return cnt


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    # print(solution.magicTower([100, 100, 100, -250, -60, -140, -50, -50, 100, 150]))
    print(solution.magicTower([5, -4, 1, -2, -2, -2, 4]))
