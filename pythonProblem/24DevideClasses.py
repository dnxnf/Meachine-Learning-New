#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：24DevideClasses.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:05
题目描述
幼儿园两个班的小朋友在排队时混在了一起，每位小朋友都知道自己是否与前面一位小朋友同班，
请你帮忙把同班的小朋友找出来小朋友的编号是整数，与前一位小朋友同班用Y表示，不同班用N表示学生序号范围(0，999]，
如果输入不合法则打印ERROR。
输入描述
输入为空格分开的小朋友编号和是否同班标志
输出描述
输出为两行，每一行记录一个班小朋友的编号，编号用空格分开，且:
1.编号需按照升序排列，分班记录中第一个编号小的排在第一行。
2.若只有一个班的小朋友，第二行为空行。
eg:
1/N 2/Y 3/N 4/Y
out:
1 2
3 4
'''
s = input()


def result():
    kids = list(map(lambda x: x.split("/"), s.split()))
    # print(kids)
    # 边界条件的判断
    if len(kids) > 999:
        print("ERROR")
        return
    one = []
    two = []
    preBelongOne = True  # 先假设属于班级1
    for kid in kids:
        idx = int(kid[0])
        # 判断这个idx
        if idx <= 0 or idx > 999:
            print("ERROR")
            return
        isSameWithPre = "Y" == kid[1]  # 与前一个相同。
        # 如果前一个属于1班。
        if preBelongOne:
            # isSameWithPre 为true
            if isSameWithPre:
                one.append(idx)
            # 与前一个为False，那么他属于2班，还要把preBelongOne(前一个属于1班)变为false，这不是属于2班了嘛
            else:
                two.append(idx)
                preBelongOne = False
        # 如果前一个不属于1班，那么前一个属于2班了。也分isSameWithPre也要分两种情况。
        else:
            if isSameWithPre:  # 与前一个相同，那么属于2班了。
                two.append(idx)
            else:  # 前一个属于2班，与前一个不同，那么就是属于1班，别忘了isSameWithPre标志要改。
                one.append(idx)
                preBelongOne = True
    # 1.编号需按照升序排列。
    one.sort()
    oneStr = " ".join(map(str, one))
    # 若只有一个班的小朋友，第二行为空行。
    if len(two) == 0:
        print(oneStr)
        print("")
        return
        # 二班不为空了
    two.sort()
    twoStr = " ".join(map(str, two))
    # 比较两个班级的第一个那个大
    if one[0] < two[0]:
        print(oneStr)
        print(twoStr)
    else:
        print(twoStr)
        print(oneStr)


result()

