# 给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
# 输出：6
# 解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。 
#  
# 
#  示例 2： 
# 
#  
# 输入：height = [4,2,0,3,2,5]
# 输出：9
#  
# 
#  
# 
#  提示： 
# 
#  
#  n == height.length 
#  1 <= n <= 2 * 10⁴ 
#  0 <= height[i] <= 10⁵ 
#  
# 
#  Related Topics 栈 数组 双指针 动态规划 单调栈 👍 5946 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def trap(self, height: List[int]) -> int:
        # 初始化双指针，分别指向数组的左右两端
        left, right = 0, len(height) - 1
        # 记录左右两侧的最大高度
        left_max, right_max = height[left], height[right]
        # 存储雨水总量
        water = 0

        # 双指针向中间移动，直到相遇
        while left < right:
            # 如果左侧高度小于右侧高度，处理左侧指针
            if height[left] < height[right]:
                # 如果当前高度大于等于左侧最大高度，更新最大高度
                if height[left] >= left_max:
                    left_max = height[left]
                # 否则，计算当前位置能存储的雨水量
                else:
                    water += left_max - height[left]
                # 左指针右移
                left += 1
            # 如果右侧高度小于等于左侧高度，处理右侧指针
            else:
                # 如果当前高度大于等于右侧最大高度，更新最大高度
                if height[right] >= right_max:
                    right_max = height[right]
                # 否则，计算当前位置能存储的雨水量
                else:
                    water += right_max - height[right]
                # 右指针左移
                right -= 1

        # 返回收集到的雨水总量
        return water

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.trap([0,1,0,2,1,0,1,3,2,1,2,1]))