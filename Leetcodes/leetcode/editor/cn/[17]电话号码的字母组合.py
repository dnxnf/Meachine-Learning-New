# 给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。 
# 
#  给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。 
# 
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：digits = "23"
# 输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
#  
# 
#  示例 2： 
# 
#  
# 输入：digits = ""
# 输出：[]
#  
# 
#  示例 3： 
# 
#  
# 输入：digits = "2"
# 输出：["a","b","c"]
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= digits.length <= 4 
#  digits[i] 是范围 ['2', '9'] 的一个数字。 
#  
# 
#  Related Topics 哈希表 字符串 回溯 👍 3092 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# 有点像全排列，回溯
class Solution:
    def letterCombinations1(self, digits: str) -> List[str]:
        dic = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }
        res = []
        # note 好牛逼的思路，先处理第一个数字，然后处理剩余数字，最后组合
        # 第一次的res是digit是[1],然后在第一个的基础上跑第二个，
        # 将第二个元素对应的字符挨个加到res里面，然后更新res
        for digit in digits:
            # 先处理第一个数字
            if not res:
                res = [char for char in dic[digit]]
            else:
                # 处理剩余数字,让当前字符与之前的字符组合，逐层递进的关系，
                # 组合完后再更新res
                tep = []
                for char in res:
                    for c in dic[digit]:
                        tep.append(char + c)
                res = tep
        return res

    def letterCombinations(self, digits: str) -> List[str]:
        # 回溯法
        if not digits:
            return []
        dic = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }
        res = []
        # path = []
        # 回溯函数,包括，当前位置，当前结果，剩余可选字符
        def backtrack(start, path, remain):
            if not remain:
                res.append(''.join(path))
                return
            # 对于当前位置，遍历剩余可选字符,也就是dic中数字对应的字符
            # 从上往下，最后一个数字对应的字符先被遍历完
            # 对于这道题，把每个字符加进去，挨个递归再回溯
            for char in dic[remain[0]]:
                path.append(char)
                backtrack(start+1, path, remain[1:])
                path.pop()
        backtrack(0, [], digits)
        return res



# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.letterCombinations("234"))
