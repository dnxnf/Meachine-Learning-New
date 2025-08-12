#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：08CurrencyTrans.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:00
记账本上记录了若千条多国货币金额，需要转换成人民币分 (fen)，汇总后输出。每行记录一条金额，
金额带有货币单位，格式为数字+单位，可能是单独元，或者单独分， 或者元与分的组合。要求将这些货币全部换算成人民币分
(fen) 后进行汇总，汇总结果仅保留整数，小数部分舍弃。元和分的换算关系都是 1:100，如下:
1CNY=100fen (1 元=100 分)
1HKD=100cents (1 港元=100 港分)
1JPY=100sen (1 日元=100 仙)
1EUR=100eurocents (1 欧元=100 欧分)
1GBP=100pence (1 英镑=100 便士)
100CNY = 1825JPY = 123HKD = 14EUR = 12GBP
输入描述
第一行输入为 N，N 表示记录数。0<N<100
之后 N 行，每行表示一条货币记录，且该行只会是一种货币。
输出描述
将每行货币转换成人民币分 (fen) 后汇总求和，只保留整数部分输出格式只有整数数字，不
带小数，不带单位。
eg:
1
123HKD
输出：10000
2
20CNY53fen
53HKD87cents
输出：6432(两个相加后）
'''
n = int(input())
arr = [input() for i in range(n)]
print(n, arr)
import re
import math
def result(n, arr):
    # \d+ 匹配一个或者多个数字。
    pattern = r"(\d+)((CNY)|(JPY)|(HKD)|(EUR)|(GBP)|(fen)|(cents)|(sen)|(eurocents)|(pence))"
    dic = {
        "CNY":100,
        "JPY": 100 / 1825 * 100,
        "HKD": 100 / 123 * 100,
        "EUR": 100 / 14 * 100,
        "GBP": 100 / 12 * 100,
        "fen": 1,
        "cents": 100 / 123,
        "sen": 100 / 1825,
        "eurocents": 100 / 14,
        "pence": 100 / 12
    }
    ans = 0
    for s in arr:
        result = re.findall(pattern, s)
        print(result)
        for item in result:
            amount = item[0]
            unit = item[1]
            ans += int(amount) * dic[unit]
    return math.floor(ans)
print(result(n, arr))
