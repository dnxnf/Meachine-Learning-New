#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：31EnglishInput.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:49
主管期望实现英文输入法单词联想功能。依据用户输入的单词前缀，从已输入的英文语句中联想出用户想输入的单词，
按字典序输出联想到的单词序列，如果联想不到，则输出用户输入的单词前缀。
注意事项：
英文单词联想时，区分大小写。
缩略形式如“don’t”，判定为两个单词，“don”和“t”。
输出的单词序列，不能有重复单词，且只能是英文单词，不能有标点符号。
二、输入描述
输入为两行：
首行输入一段由英文单词 word 和标点符号组成的语句 str。
接下来一行为一个英文单词前缀 pre。
约束条件：
0 < word.length ≤ 20。
0 < str.length ≤ 1000。
0 < pre ≤ 20。
三、输出描述
输出符合要求的单词序列或单词前缀，存在多个时，单词之间以单个空格分割。
eg:
I love you
He
out:He
------------
The furthest distance in the world, Is not between life
and death, But when I stand in front of you, Yet you
don't know that I love you.
f
out:front furthest
'''
s = input()
pre = input()
print(s)
'''
The furthest distance in the world, Is not between life and death, But when I stand in front of you, Yet you don't know that I love you.
f
'''
print(pre)
import re
def result():
    tmp = re.split("[^a-zA-Z]", s) # 非大小写字母，就是分隔符。
    cache = list(set(tmp))
    cache.sort()
    # 把前缀过滤出来
    cache = list(filter(lambda x:x.startswith(pre), cache))
    if len(cache) == 0:
        return pre
    else:
        # len(cache) != 0
        return " ".join(cache)
print(result())
