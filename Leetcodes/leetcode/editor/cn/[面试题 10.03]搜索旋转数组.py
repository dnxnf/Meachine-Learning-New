# 搜索旋转数组。给定一个排序后的数组，包含n个整数，但这个数组已被旋转过很多次了，次数不详。请编写代码找出数组中的某个元素，假设数组元素原先是按升序排列的。若
# 有多个相同元素，返回索引值最小的一个。 
# 
#  示例 1： 
# 
#  
#  输入：arr = [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], target = 5
#  输出：8（元素5在该数组中的索引）
#  
# 
#  示例 2： 
# 
#  
#  输入：arr = [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], target = 11
#  输出：-1 （没有找到）
#  1, 3, 4, 5, 7, 10, 14, 15, 16, 19, 20, 25
# 
#  提示: 
# 
#  
#  arr 长度范围在[1, 1000000]之间 
#  
# 
#  Related Topics 数组 二分查找 👍 140 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def search_wrong(self, arr: List[int], target: int) -> int:
        # 二分查找，中间值大于等于target，则左边查找，中间值小于target，在右边查找
        # 不对，因为当重复元素太多时，会出现问题
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                if arr[left] <= target < arr[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if arr[mid] < target <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1
    def search(self, arr: List[int], target: int) -> int:
        # 二分查找，中间值大于等于target，则左边查找，中间值小于target，在右边查找
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return -1
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)