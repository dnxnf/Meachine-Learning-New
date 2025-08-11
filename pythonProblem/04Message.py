#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：04Message.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午9:14
IGMP协议中，有一个字段称作最大响应时间(Max Response Time),HOST收到查询报文，
解折出MaxResponsetime字段后，需要在[0,MaxResponseTime]时间(s)内选取随机时间回应一个响应报文，
如果在随机时间内收到一个新的查询报文，则会根据两者时间的大小，选取小的一方刷新回应时间。
最大响应时间有如下计算方式：
当Max Resp Code <128, Max Resp Time = Max Resp Code;
当Max Resp Code≥128,
Max Resp Time =(mant|0x10)<<(exp+3);注：exp最大响应时间的高5~7位mant为最大响应时间的低4位。
其中接收到的MaxRespCode最大值为255,以上出现所有字段均为无符号数。
现在我们认为HOST收到查询报文时，选取的随机时间必定为最大值，现给出HOST收到查询报文个数C,HOST收到该报文的时间T,
以及查询报文的最大响应时间字段值M,请计算出HOST发送响应报文的时间。
输入描述
第一行为查询报文个数C, 后续每行分别为HOST收到报文时间T,及最大响应时间M,以空格分割。
输出描述
HOST发送响应报文的时间。
备注用例确定只会发送一个响应报文，不存在计时结束后依然收到查询报文的情况。
用例
输入
3
0 20
1 10
8 20
输出
11
说明
收到3个报文，
第0秒收到第1个报文，响应时间为20秒，则要到0+20=20秒响应；
第1秒收到第2个报文，响应时间为10秒，则要到1+10=11秒响应，与上面的报文的响应时间比较获得响应时间最小为11秒；
第8秒收到第3个报文，响应时间为20秒，则要到8+20=28秒响应，与第上面的报文的响应时间比较获得响应时间最小为11秒；
最终得到最小响应报文时间为11秒
'''
import sys

# 输入获取
c = int(input())
messages = [list(map(int, input().split())) for _ in range(c)]
def getMaxResponseTime(m):
    if m >= 128:
        bStr = bin(m)[2:]

        while len(bStr) < 8:
            bStr = '0' + bStr

        exp = int(bStr[1:4], 2)
        mant = int(bStr[4:], 2)

        return (mant | 16) << (exp + 3)
    else:
        return m

# 算法入口
def getResult():
    ans = sys.maxsize

    for t, m in messages:
        respTime = t + getMaxResponseTime(m)
        ans = min(ans, respTime)

    return ans


# 算法调用
print(getResult())