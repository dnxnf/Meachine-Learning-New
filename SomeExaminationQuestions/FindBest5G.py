#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from collections import deque

cross = list(map(int, input().split()))
k = int(input())
n = len(cross)
ret = []
q = deque()

# 路段i对应基站范围 [i+1-k, i+k]
for i in range(n - 1):
    left = max(0, i + 1 - k)
    right = min(n - 1, i + k)

    # 移除不在当前窗口的元素
    while q and q[0] < left:
        q.popleft()

    # 添加新元素到队列（保持递增顺序）
    # 需要从left到right依次处理
    for j in range(left, right + 1):
        while q and cross[j] <= cross[q[-1]]:
            q.pop()
        q.append(j)

    # 当前窗口的最小值在队列头部
    ret.append(str(q[0]))

print(' '.join(ret))
