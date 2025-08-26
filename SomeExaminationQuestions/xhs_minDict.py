#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：xhs_minDict.py
@Description ： 没写出来
给定一个长度为 n 的字符串 s，该字符串仅由小写字母构成。
你需要删除尽可能少的字符，使得所得的字符串中，字符‘a’至‘z’的出现次数满足：
‘a’的次数<=‘b’的次数<= ‘z’的次数,且字典序最小。
输入描述
第一行输入一个整数 n(1≤n≤2×105)，表示字符串长度。
第二行输入一个长度为 n,仅由小写字母构成的字符串 s。除此之外，保证字符串至少包含一个'z'。
输出描述
输出一个字符串，表示满足上述条件且字典序最小的结果字符串。
in:
4
xyxz
输出：xyz
@Author      ：Hello World
@Date        ：2025/8/24 下午8:17 
'''


# 先满足非严格递增，再字典序最小
# 字典序最小：先按字母顺序排序，再按字母出现次数排序,z的字典序最小
# 非严格递增：a出现次数<=b出现次数<=z出现次数
def solve(n, s):
    dict = {}
    for c in s:
        dict[c] = dict.get(c, 0) + 1
    dict = sorted(dict.items(), key=lambda x: (x[0], -x[1]), reverse=True)
    print(dict)
    # 最多保留多少
    max_count = dict[0][1]
    dict_del = {}
    for i in range(1, len(dict)):
        if dict[i][1] > max_count:
            dict_del[dict[i][0]] = dict[i][1] - max_count
    print(dict_del)
    # 拿得到的开始删除
    # 用dict_del删除s,倒着删除
    res = ''
    for c in s[::-1]:
        if c in dict_del:
            dict_del[c] -= 1
            if dict_del[c] == 0:
                del dict_del[c]
        else:
            res += c
    return res[::-1]


def submit():
    n = int(input())
    s = input()
    print(solve(n, s))


# submit()


# what 这个思路想法，因为前面的每个字母数量小于后面的字母数量，所以可以先统计每个字母出现的次数，
# 然后从后向前调整，确保后面的次数不小于前面的，这样记载的就是最终可以用的字符数量
# 然后现在已经记录了每个字母可以使用的数量，那么从前往后遍历，
# 如果当前字符的数量小于后面的字符的数量，那么就选择这个字符，
def solve2(n, s):
    # 统计每个字符的出现次数
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1

    # 目标：让count[0] <= count[1] <= ... <= count[25]
    # 从后向前调整，确保后面的次数不小于前面的
    tep = 0
    for i in range(25, -1, -1):  # 从y到a
        if count[i] > 0:
            tep = count[i]
        break
    print(count)
    print(tep)
    # 从'z'向前调整，确保每个字符的次数不超过后面字符的次数
    # 现在tep是字典序最大的个数，其他每个都要小于这个
    for i in range(24, -1, -1):  # 从y到a
        if count[i] > tep:
            count[i] = tep
            tep = count[i]
        elif count[i] == tep:
            continue
        elif count[i] < tep and count[i] != 0:
            tep = count[i]

    print(count)
    # 现在我们需要构建结果字符串，尽可能保留字典序小的字符
    # 但需要满足调整后的次数限制

    result = []
    # 记录当前已经使用的每个字符的数量
    used = [0] * 26

    # xzaxa xza
    # zaxa zax

    for c in s:
        idx = ord(c) - ord('a')
        # 如果这个字符还可以使用（不超过调整后的限制）
        if used[idx] < count[idx]:
            # 检查是否可以选择这个字符（贪心选择字典序最小的）
            # 同时要确保后面的字符有足够的空间
            result.append(c)
            used[idx] += 1
        # 否则跳过这个字符

    return ''.join(result)


def submit2():
    n = int(input())
    s = input()
    print(solve2(n, s))


submit2()
