#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def solve(n, d):
    # 计算每个节点能访问到的服务点位置
    # 节点i可以访问到位置j，如果 |i-j| <= d[i]
    # 注意：题目中节点编号从1开始
    can_reach = []
    for i in range(n):
        node_id = i + 1  # 节点编号从1开始
        reachable = set()
        for j in range(1, n + 1):  # 服务点可能的位置
            if abs(node_id - j) <= d[i]:
                reachable.add(j)
        can_reach.append(reachable)

    # 使用贪心算法：每次选择能被最多未覆盖节点访问到的位置
    covered = set()  # 已经被覆盖的节点
    service_points = 0

    while len(covered) < n:
        best_pos = -1
        best_coverage = set()

        # 找到能被最多未覆盖节点访问到的位置
        for pos in range(1, n + 1):  # 服务点可能的位置
            if pos not in covered:  # 如果这个位置还没有被覆盖
                # 计算有多少未覆盖的节点可以访问到这个位置
                can_access = set()
                for i in range(n):
                    if (i + 1) not in covered and pos in can_reach[i]:
                        can_access.add(i + 1)

                if len(can_access) > len(best_coverage):
                    best_coverage = can_access
                    best_pos = pos

        if best_pos == -1 or len(best_coverage) == 0:
            break

        # 选择这个位置作为服务点
        service_points += 1
        covered.update(best_coverage)

    return service_points


# 测试第一个例子
n = 7
d = [4, 0, 0, 1, 3, 1, 3]
result = solve(n, d)
print(f"n={n}, d={d}")
print(f"结果: {result}")
print(f"期望: 3")
print(f"正确: {'✓' if result == 3 else '✗'}")

# 打印每个节点能访问到的位置
print("\n每个节点能访问到的位置:")
for i in range(n):
    node_id = i + 1
    reachable = []
    for j in range(1, n + 1):
        if abs(node_id - j) <= d[i]:
            reachable.append(j)
    print(f"节点{node_id}: {reachable}")
