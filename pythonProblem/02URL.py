#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：02URL.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午9:02
给定一个URL前缀和URL后缀，通过逗号分割。需要将其连接为一个完整的URL。拼接规则如下：
若前缀结尾和后缀开头都没有/，则自动补上/连接符；
若前缀结尾和后缀开头都为/，则需去重保留一个；
无需考虑前后缀的合法性（例如输入为空或特殊字符）。
输入描述
输入为一行字符串，包含URL前缀和后缀，用逗号分隔。例如：/acm,/bb。
前缀和后缀长度均小于100。
输出描述
拼接后的完整URL。若前后缀均为空，则输出/。
/acm,/bb
输出
/acm/bb
'''


def join_url(prefix, suffix):
    # 处理前缀和后缀均为空的情况
    if not prefix and not suffix:
        return '/'
    # 处理前缀的结尾斜杠和后缀的开头斜杠
    if prefix.endswith('/') and suffix.startswith('/'):
        suffix = suffix[1:]
    elif not prefix.endswith('/') and not suffix.startswith('/'):
        if prefix or suffix:  # 至少有一个非空才加/
            suffix = '/' + suffix

    return prefix + suffix
# 读取输入
input_str = input().strip()
prefix, suffix = input_str.split(',', 1)  # 只分割第一个逗号
# 调用函数并输出结果
print(join_url(prefix, suffix))