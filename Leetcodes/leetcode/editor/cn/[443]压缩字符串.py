# 给你一个字符数组 chars ，请使用下述算法压缩： 
# 
#  从一个空字符串 s 开始。对于 chars 中的每组 连续重复字符 ： 
# 
#  
#  如果这一组长度为 1 ，则将字符追加到 s 中。 
#  否则，需要向 s 追加字符，后跟这一组的长度。 
#  
# 
#  压缩后得到的字符串 s 不应该直接返回 ，需要转储到字符数组 chars 中。需要注意的是，如果组长度为 10 或 10 以上，则在 chars 数组中会
# 被拆分为多个字符。 
# 
#  请在 修改完输入数组后 ，返回该数组的新长度。 
# 
#  你必须设计并实现一个只使用常量额外空间的算法来解决此问题。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：chars = ["a","a","b","b","c","c","c"]
# 输出：返回 6 ，输入数组的前 6 个字符应该是：["a","2","b","2","c","3"]
# 解释："aa" 被 "a2" 替代。"bb" 被 "b2" 替代。"ccc" 被 "c3" 替代。
#  
# 
#  示例 2： 
# 
#  
# 输入：chars = ["a"]
# 输出：返回 1 ，输入数组的前 1 个字符应该是：["a"]
# 解释：唯一的组是“a”，它保持未压缩，因为它是一个字符。
#  
# 
#  示例 3： 
# 
#  
# 输入：chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
# 输出：返回 4 ，输入数组的前 4 个字符应该是：["a","b","1","2"]。
# 解释：由于字符 "a" 不重复，所以不会被压缩。"bbbbbbbbbbbb" 被 “b12” 替代。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= chars.length <= 2000 
#  chars[i] 可以是小写英文字母、大写英文字母、数字或符号 
#  
# 
#  Related Topics 双指针 字符串 👍 435 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    # 双指针法
    def compress(self, chars: List[str]) -> int:
        if not chars:
            return 0

        write = 0  # 写入位置
        read = 0  # 读取位置
        n = len(chars)

        while read < n:
            current_char = chars[read]
            count = 0

            # 统计当前字符的连续出现次数
            while read < n and chars[read] == current_char:
                read += 1
                count += 1

            # 写入当前字符
            chars[write] = current_char
            write += 1

            # 如果次数大于1，写入次数
            if count > 1:
                for digit in str(count):
                    chars[write] = digit
                    write += 1

        return write

    # def compress(self, chars: List[str]) -> int:
    #     # 我的，没写完
    #     dic = {}
    #     res = []
    #     for i in chars:
    #         if i in dic:
    #             dic[i] += 1
    #         else:
    #             dic[i] = 1
    #     # print(dic)
    #     for i in dic.keys():
    #         # print(i)
    #         if dic[i] == 1:
    #             dic[i] = ''
    #         elif dic[i] > 1:
    #             dic[i] = str(dic[i])
    #     # print(dic) #全都是字符
    #
    #     sum = 0
    #     for k, v in dic.items():
    #         res.append(k)
    #         if v != '':
    #             res.append(v)
    #     #         全都加到列表里后，相加列表所有元素的长度
    #     for i in res:
    #         sum += len(i)
    #     index = 0
    #     for item in res:
    #         for c in item:
    #             if index < len(chars):
    #                 chars[index] = c
    #                 index += 1
    #             else:
    #                 # 如果 chars 长度不足，需要扩展（但题目要求原地修改，假设 chars 足够长）
    #                 chars.append(c)
    #
    #     return sum
    # def compress(self, chars: List[str]) -> int:
    #     #         看完答案代码之后重写的
    #     # 一个写入数字的，一个读取数字的
    #     if not chars:
    #         return 0
    #     write = 0
    #     read = 0
    #     n = len(chars)  # 因为长度会改变
    #     while read < n:  # 读取完之前
    #         cur = chars[read]
    #         count = 0
    #         # 看有几个相同的
    #         while read < n and chars[read] == cur:
    #             read += 1
    #             count += 1
    #         chars[write] = cur
    #         write += 1
    #         if count > 1:
    #             for digit in str(count):
    #                 chars[write] = digit
    #                 write += 1
    #     return write


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.compress(["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]))
