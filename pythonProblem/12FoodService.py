#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：12FoodService.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:21
题目描述：
某公司员工食堂以盒饭方式供餐。为将员工取餐排队时间降低为0，食堂的供餐速度必须要足够快。现在需要根据以往员工取餐的统计信息，
计算出一个刚好能达成排队时间为0的最低供餐速度。即，食堂在每个单位时间内必须至少做出多少份盒饭才能满足要求。
输入描述:
第1行为一个正整数N，表示食堂开餐时长。1 <= N <= 1000。
第2行为一个正整数M，表示开餐前食堂已经准备好的盒饭份数。pi <= M <= 1000.
第3行为N个正整数，用空格分隔，依次表示开餐时间内按时间顺序每个单位时间进入食堂取餐的人数Pi。1 <=i<= N，0<= Pi<=100.
输出描述:
个整数，能满足题目要求的最低供餐速度(每个单位时间需要做出多少份盒饭)
补充说明:
每人只取一份盒饭。
需要满足排队时间为0，必须保证取餐员工到达食堂时，食堂库存盒饭数量不少于本次来取餐的人数。第一个单位时间来取餐的员工只能取开
餐前食堂准备好的盒饭。每个单位时间里制作的盒饭只能供应给后续单位时间来的取餐的员工食堂在每个单位时间里制作的盒饭数量是相同的。
示例1
输入:
3
14
10 4 5
输出:
3
'''
n = int(input())
m = int(input())
# 3
# 14
# 10 4 5
p = list(map(int, input().split()))
print(n, m)
print(p)
def check(m, add, p):
    # m初始饭盒数量。add是单位时间内增加的数量。p是排队人数的序列
    m -= p[0] #第一批肯定是够了，题目保证 P1≤M≤1000
    # 开始取餐
    for i in range(1, len(p)):
        m += add # 增加了人
        if m >= p[i]:
            # 能满足p[i]的需求
            m -= p[i]
        # 不能满足需求只能false
        else:
            return False
    # 都遍历完了。可以返回True
    return True

def result():
    # 最小值是0，最大值是max(p)
    l, r = 0, max(p)
    ans = 0
    while l <= r:
        mid = (l + r) // 2 # 平时习惯性的写成m了，但是本题已经占用m了。所以。
        if check(m, mid, p):
            # 满足的话mid 可能是题解，先记录下。
            ans = mid
            # 继续找更有优的解
            r = mid - 1
        else:
            l = mid + 1
    return ans
result()