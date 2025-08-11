# 给你一个字符串 word 和一个整数 numFriends。
#
#  Alice 正在为她的 numFriends 位朋友组织一个游戏。游戏分为多个回合，在每一回合中：
#
#
#  word 被分割成 numFriends 个 非空 字符串，且该分割方式与之前的任意回合所采用的都 不完全相同 。
#  所有分割出的字符串都会被放入一个盒子中。
#
#
#  在所有回合结束后，找出盒子中 字典序最大的 字符串。
#
#
#
#  示例 1：
#
#
#  输入: word = "dbca", numFriends = 2
#
#
#  输出: "dbc"
#
#  解释:
#
#  所有可能的分割方式为：
#
#
#  "d" 和 "bca"。
#  "db" 和 "ca"。
#  "dbc" 和 "a"。
#
#
#  示例 2：
#
#
#  输入: word = "gggg", numFriends = 4
#
#
#  输出: "g"
#
#  解释:
#
#  唯一可能的分割方式为："g", "g", "g", 和 "g"。
#
#
#
#  提示:
#
#
#  1 <= word.length <= 5 * 10³
#  word 仅由小写英文字母组成。
#  1 <= numFriends <= word.length
#
#
#  Related Topics 双指针 字符串 枚举 👍 19 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 双指针
class Solution:
    def answerString(self, word: str, num: int) -> str:
        if num == 1:
            return word
        n = len(word)
        res = ""
        maxn = len(word) - (num - 1)
        for i in range(n):
            # 有多的就往后写，没有就到末尾
            res = max(res, word[i: min(i + maxn, n)])
        return res

        # if num == 1:
        #     return word
        # start = 0
        # # 最多有这么多字符
        # maxn = len(word) - (num - 1)
        # for i in range(len(word)):
        #     if word[start] < word[i]:
        #         start = i
        # print('word[start]',word[start])
        # res = []
        # res.append(word[start])
        # cnt = min(maxn,len(word)-start)
        # print(cnt)
        # # length = 1
        # for i in range(1,cnt):
        #     res.append(word[start+i])
        #     # start+=1
        # print(res)
        # return "".join(res)

        # return start
        # 最长的子串
    #     下面的是最长的，有点问题，字典排序是以最大的起始
    #     # print(ord('a'),ord('z')) # 97 122
    #     # 要尽可能长,最长子串的长度
    #     # 有num-1个为1，其他的为一组
    #     maxn = len(word) - (num - 1)
    #     # 前maxn个字符
    #     res = [word[0:maxn]]
    #     # for i in range(maxn):
    #     #     res.append(word[i])
    #     print(res)
    #     right = 0
    #     left = maxn - 1
    #     for i in range(maxn, len(word)):
    #         right += 1
    #         left += 1
    #         res.append(word[right:left+1])
    #         # print(res)
    #     # 找出最大的
    #     ans = res[0]
    #     for i in range(1,len(res)):
    #         if ans < res[i]:
    #             ans = res[i]
    #     return ans
    # # def getListOrd


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.answerString("dbca", 2))
