#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：30MemoryPool.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:43
请实现一个简易内存池,根据请求命令完成内存分配和释放，内存池支持两种操作命令，REQUEST和RELEASE，其格式为:
REQUEST=请求的内存大小表示请求分配指定大小内存，如果分配成功，返回分配到的内存首地址，如果内存不足，或指定的大小为0，则输出error。
RELEASE=释放的内存首地址表示程放掉之前分配的内存，释放成功无需输出，如果释放不存在的首地址则输出error.
注意:
1.内存池总大小为100字节
2.内存池地址分配必须是连续内存，并优先从低地址分配
3.内存释放后可被再次分配，已释放的内存在空闲时不能被二次释放。
4.不会释放已申请的内存块的中间地址。
5.释放操作只是针对首地址所对应的单个内存块进行操作，不会影响其它内存块。
输入描述
首行为整数N,表示操作命令的个数，取值范围:0<N<=100接下来的N行，每行将给出一个操作命令，操作命令和参数之间用“=”分割.
输出描述
请求分配指定大小内存时，如果分配成功，返回分配到的内存首地址，如果内存不足，
或指定的大小为0，则输出error释放掉之前分配的内存时，释放成功无需输出，如果释放不
存在的首地址则输出error。
eg:
2
REQUEST=10
REQUEST=20
out:
0
10
'''
'''
5
REQUEST=10
REQUEST=20
RELEASE=0
REQUEST=20
REQUEST=10
'''
n = int(input())
cmds = [input().split("=") for i in range(n)]
print(n)
print(cmds)
def isInter(a1, a2):
    s1, e1 = a1
    s2, e2 = a2
    if s1 == s2:
        return True
    elif s1<s2:
        return e1>=s2
    else:
        # s1>s2
        return e2>=s1

# 算法入口
def result():
    # used 保存被占用的内存 [起始地址，结束地址]，初始时有一个[100,101]作为尾边界限定
    used =[[100, 101]] # 题目说了最大就100，就是0-99嘛
    for key ,val in cmds:
        # 申请内存
        if key == "REQUEST":
            # 当指令为 REQUEST 时，对应值为要申请的内存的大小，即 size
            size = int(val)
            # 开始位置从0 开始检查，有没有可用的空间。
            start = 0
            flag = True
            for i in range(len(used)):
                end = start+size-1 # [start, end] 都是闭区间，所以
                # 需要申请的区间
                ran = [start, end]
                # 检查要申请的内存区间和已占有的内存区间是否交叉
                if not isInter(used[i], ran):
                    # 若不存在交叉，则将申请区间加入 used 中
                    used.insert(i, ran)
                    flag = False
                    # 并打印此时申请区间的起始位置
                    print(start)
                    break
                else:
                    # 若存在交叉，则将变更要申请的内存区间的起始位置
                    start = used[i][1] + 1 # 记得加1，不然还是重叠。
            # 一旦申请到内存，那么 flag 就会被赋值为 false，否则就保持 true，意味着没申请到内存，则打印error
            if flag:
                # 搞了一圈了，还没申请到内存
                print("error")
        # 释放内存。
        else:
            # key == "REQUEST" 当指令为 RELEASE 时，值为要释放内存的起始地址 addr
            addr = int(val)
            # 那我就要去找首地址对应的区间呀
            flag = True
            for i in range(len(used)):
                # 到已占有内存中找起始位置是 addr 的，找到则将该区间从 used 中删除，表示解除占用
                if used[i][0] == addr:
                    used.pop(i) # 这个厉害。我一般用的多的是pop(0)
                    flag = False
                    break
            if flag:
                # 找了一圈没找到。只能返回error了
                print("error")
# print(result())
result()