#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：23ComputerArray.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:57
小明正在规划一个大型数据中心机房，为了使得机柜上的机器都能正常满负荷工作，需要确保在每个机柜边上至少要有一个电箱。
为了简化题目，假设这个机房是一整排，M表示机柜，I表示间隔，要求返回整排机柜至少需要多少个电箱。如果无解则返回-1。
二、输入描述
一个字符串cabinets，其中M表示机柜，I表示间隔。字符串长度满足1 ≤ strlen(cabinets) ≤ 10000。
例如：cabinets = "MIIM"
其中M表示机柜，I表示间隔
三、输出描述
返回整排机柜至少需要多少个电箱。
2,表示至少需要2个电箱
补充说明：
1<= strlen(cabinets) <= 10000
其中 cabinets[i] = ‘M’ 或者 ‘I’
示例
输入：
MIIM
输出:2
'''
def result():
    n = len(s)
    ans = 0
    i = 0
    while i < n:
        if s[i] == "M":
            # 如果当前为机柜
            # 优先将电箱放到机柜的右边，如果机柜右边有间隔I的话，还要别越界
            if i+1<n and s[i+1] == "I":
                ans += 1
                # 如果放成功了的话，第i个位置为机柜，i+1的位置为电箱
                # 那么第i+2无论是机柜，还是空位，还是电箱都可以。所以这里i+2
                i += 2 # 注意要理解这个。
            # 上面右边搞不定，我们只能搞左边了。
            elif i-1>0 and s[i-1] == "I":
                # 如果左边没越界，并且左边有空位
                ans += 1
            # 两边都搞不定，只能返回无法放入电箱了
            else:
                ans = -1
                break
        i += 1 #往后走一个了。
    return ans
s = input()
print(result())
