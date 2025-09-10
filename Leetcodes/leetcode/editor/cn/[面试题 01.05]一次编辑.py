# 字符串有三种编辑操作:插入一个英文字符、删除一个英文字符或者替换一个英文字符。 给定两个字符串，编写一个函数判定它们是否只需要一次(或者零次)编辑。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：
# first = "pale"
# second = "ple"
# 输出：True 
# 
#  
# 
#  示例 2： 
# 
#  
# 输入：
# first = "pales"
# second = "pal"
# 输出：False
#  
# 
#  Related Topics 双指针 字符串 👍 268 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def oneEditAway(self, first: str, second: str) -> bool:
        if len(first) - len(second) > 1 or len(second) - len(first) > 1:
            return False
        if len(first) == len(second):
            count = 0
            for i in range(len(first)):
                if first[i] != second[i]:
                    count += 1
                    if count > 1:
                        return False
            return True
        # 相差为1
        else:
            # 只相差一个字符，只能删或者增加
            i, j = 0, 0
            cnt = 0
            if len(first) == len(second) + 1:
                while i < len(first) and j < len(second):
                    if first[i] != second[j]:
                        i += 1
                        cnt += 1
                        if cnt > 1:
                            return False
                    else:
                        i += 1
                        j += 1
                return True
            elif len(first) == len(second) - 1:
                while i < len(first) and j < len(second):
                    if first[i] != second[j]:
                        j += 1
                        # j += 1
                        cnt += 1
                        if cnt > 1:
                            return False
                    else:
                        i += 1
                        j += 1
                return True

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
