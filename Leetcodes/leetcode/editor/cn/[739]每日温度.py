# 给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天，下一个更高温度出现
# 在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: temperatures = [73,74,75,71,69,72,76,73]
# 输出: [1,1,4,2,1,1,0,0]
#  
# 
#  示例 2: 
# 
#  
# 输入: temperatures = [30,40,50,60]
# 输出: [1,1,1,0]
#  
# 
#  示例 3: 
# 
#  
# 输入: temperatures = [30,60,90]
# 输出: [1,1,0] 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= temperatures.length <= 10⁵ 
#  30 <= temperatures[i] <= 100 
#  
# 
#  Related Topics 栈 数组 单调栈 👍 1975 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)

# favour 单调栈
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        #1e5，n方不行
        ans = [0] * len(temperatures)
        # 使用栈来保存尚未找到更高温度的日期索引
        stack = []
        for i in range(len(temperatures)):
            # 当前温度比栈顶温度高时，说明找到了栈顶日期的更高温度
            while stack and temperatures[i] > temperatures[stack[-1]]:
                j = stack.pop()
                ans[j] = i - j
            stack.append(i)
        return ans
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.dailyTemperatures([73,74,75,71,69,72,76,73]))