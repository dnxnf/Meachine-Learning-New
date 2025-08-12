#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：17StringJudge.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:37
题目描述
输入两个字符串S和L，都只包含英文小写字母。S长度<=100，L长度<=500,000。判定S是否是L的有效字串。
判定规则：S中的每个字符在L中都能找到（可以不连续），且S在Ｌ中字符的前后顺序与S中顺序要保持一致。（例如，S="ace"是L="abcde"的一个子序列且有效字符是a、c、e，而"aec"不是有效子序列，且有效字符只有a、e）
输入描述
输入两个字符串S和L，都只包含英文小写字母。S长度<=100，L长度<=500,000。先输入S，再输入L，每个字符串占一行。
输出描述
S串最后一个有效字符在L中的位置。（首位从0开始计算，无有效字符返回-1）
补充说明
示例1
输入：
ace
abcde
输出:4
-------------
fgh
abcde
out:-1
'''


def main():
    s = input()
    l = input()
    # 初始化last_idx为-1，表示找不到时的返回值
    last_idx = -1
    # 初始化匹配位置为0
    to_match = 0
    m = len(s)
    n = len(l)

    # 遍历字符串l
    for i in range(n):
        if to_match < m and s[to_match] == l[i]:
            # 增加匹配的位置
            to_match += 1
            # 更新最后匹配的索引
            last_idx = i
        if to_match >= m:
            break
    print(last_idx)


if __name__ == "__main__":
    main()