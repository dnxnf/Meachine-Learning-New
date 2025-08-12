#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：35CharCount.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午11:33
写出一个程序，接受一个由字母、数字和空格组成的字符串，和一个字符，然后输出 输入字符串Q中该字符的出现次数。（不区分大小
写字母）。
输入描述
第一行输入一个由字母、数字和空格组成的字符串，第二行输入一个字符（保证该字符不为空格）。
输出描述
输出输入字符串中含有该字符的个数, (不区分大小写字母)。
用例1
Hello World
o
out:2
'''
# 读取第一行输入：由字母、数字和空格组成的字符串
input_string = input()

# 读取第二行输入：目标字符（保证不为空格）
target_char = input()

# 将输入字符串和目标字符都转换为小写，实现不区分大小写的比较
lower_input_string = input_string.lower()
lower_target_char = target_char.lower()

# 初始化计数器，用于统计目标字符的出现次数
count = 0

# 遍历输入字符串的每个字符
for char in lower_input_string:
    # 如果当前字符与目标字符相同，计数器加1
    if char == lower_target_char:
        count += 1

# 输出目标字符在输入字符串中的出现次数
print(count)
