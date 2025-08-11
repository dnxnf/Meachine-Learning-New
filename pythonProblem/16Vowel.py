#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：16Vowel.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:35
开头和结尾都是元音字母（aeiouAEIOU）的字符串为元音字符串，其中混杂的非元音字母数量为其瑕疵度。比如:
“a” 、 “aa” 是元音字符串，其瑕疵度都为0
“aiur” 不是元音字符串（结尾不是元音字符）
“abira” 是元音字符串，其瑕疵度为2
给定一个字符串，请找出指定瑕疵度的最长元音字符子串，并输出其长度，如果找不到满足条件的元音字符子串，输出0。
子串：字符串中任意个连续的字符组成的子序列称为该字符串的子串。
输入描述
首行输入是一个整数，表示预期的瑕疵度flaw，取值范围[0, 65535]。
接下来一行是一个仅由字符a-z和A-Z组成的字符串，字符串长度(0, 65535]。
输出描述
输出为一个整数，代表满足条件的元音字符子串的长度。
示例1
输入：
0
asdbuiodevauufgh
输出：
3
说明：满足条件的最长元音字符子串有两个，分别为uio和auu，长度为3。
示例2
输入：
2
aeueo
输出：
0
说明：没有满足条件的元音字符子串，输出0
'''
import string

def solve(flaw: int, s: string) -> int:
    """找出指定瑕疵度的最长元音字符子串，并返回其长度"""
    n = len(s)
    flaw_cnt = [0] * (n + 1)    # 瑕疵度表, flaw_cnt[x] 表示前 s[:x] 的瑕疵度
    vowels = set("aeiouAEIOU")
    vowel_idxs = []             # 元音字符下标列表

    cnt = 0
    for i, c in enumerate(s):
        if c in vowels:  # 元音字符
            vowel_idxs.append(i)
        else:  # 非元音字母:  瑕疵度 + 1
            cnt += 1
        flaw_cnt[i + 1] = cnt

    l, max_length = 0, 0
    for r in range(len(vowel_idxs)):
        right = vowel_idxs[r]
        while l <= r:
            left = vowel_idxs[l]
            # 计算区间内的瑕疵度
            cur_flaw = flaw_cnt[right + 1] - flaw_cnt[left]
            if cur_flaw > flaw:  # 比预期的瑕疵度大，则左侧指针右移缩小窗口
                l += 1
                continue
            if cur_flaw == flaw:
                max_length = max(max_length, right - left + 1)
            break

    return max_length


if __name__ == "__main__":
    flaw = int(input())
    s = input()
    print(solve(flaw, s))

