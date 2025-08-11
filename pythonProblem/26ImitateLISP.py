#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：26ImitateLISP.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:14
LISP 语言唯一的语法就是括号要配对。 形如(OP P1 P2 …)，括号内元素由单个空格分割。 其中第一个元素 OP 为操作符，
后续元素均为其参数，参数个数取决于操作符类型
注意：参数 P1, P2 也有可能是另外一个嵌套的(OP P1 P2 …) 当前 OP 类型为 add / sub / mul / div（全小写），
分别代表整数的加减乘除法简单起见，所有 OP 参数个数均为 2
题目涉及数字均为整数，可能为负；
不考虑 32 位溢出翻转，计算过程中也不会发生 32 位溢出翻转 除零错误时，输出 “error”；
除法遇除不尽，向下取整，即 3 / 2 = 1
输入描述：
输入为长度不超过 512 的字符串，用例保证了无语法错误
输出描述：
输出计算结果或者“error”
eg:
(mul 3 -7)
out:-21
------------------------
(sub (mul 2 4) (div 9 3))
out:5
'''
s = input()
import math


def oper(op, p1, p2):
    p1 = int(p1)
    p2 = int(p2)
    if op == "add":
        return str(p1 + p2)
    elif op == "sub":
        return str(p1 - p2)
    elif op == "mul":
        return str(p1 * p2)
    elif op == "div":
        if p2 == 0:
            return "error"
        else:
            # return str(p1//p2)
            return str(int(math.floor(p1 / p2)))
    else:
        return "error"


def result():
    stack = []
    leftIdxs = []
    for i in range(len(s)):
        if s[i] == ")":
            l = leftIdxs.pop()  # 找到栈里最近的"("
            fragment = stack[l:]  # 截取片段。
            del stack[l:]  # 在栈中删除。
            # fragment[0] = "("
            # 这里fragment是list，所以要拼接下。然后再用
            # print("fragment:", fragment)
            op, p1, p2 = "".join(fragment[1:]).split(" ")
            res = oper(op, p1, p2)
            if res == "error":
                return "error"
            else:
                print(res)
                stack.extend(list(res))  # 不就是一个字符嘛，还要转化为列表，然后还要list下？
        elif s[i] == "(":
            # 等于"(" 要记录当前的位置啊
            leftIdxs.append(len(stack))  # 把当前长度加上去，这样的话他刚好下标加1
            stack.append(s[i])
        else:
            stack.append(s[i])
    return "".join(stack)


# s='(div 12 (sub 45 45))' # 输出'error'
# s = '(add 1 (div -7 3))'
result()
