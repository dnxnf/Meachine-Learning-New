#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project     ：MachineLearning
@File        ：xhs_serverNode.py
@Description ：小红书后端基础设施包含 n 个服务器节点，编号 1 到 n。
第i个节点与相邻节点（即编号 i-1 和 i+1 的节点，如果存在）通过链路相连。
每一个节点都有它的传输信号限制，第i个节点发送的数据至多只能经过 di 条链路。
现需在若干节点部署服务点，确保每个节点均可在不超过其链路限制的
范围内访问到至少一个服务点。求最少需要部署的服务点数。
输入描述
每个测试文件均包含多组测试数据。第一行输入一个整数 T(1<T<10^4)代表数据组数,每组测试数据描述如下:
第一行输入一个整数 n (1<=n<2*10^5) ，表示节点数。
第二行输入n个整数d1,d2……dn (0<=di<=10^5)，表示第i个节点的传输信号限制。
除此之外,保证单个测试文件的 n之和不超过2*10^5
输出描述
对于每组测试数据,输出一个整数,表示最少需要部署的服务点数。
input:
3
7
4 0 0 1 3 1 3
5
0 1 1 1 0
4
0 0 0 0
output:
3
3
4
样例解释
对于第一组测试数据,节点覆盖区间分别为[1, 5],[2, 2],
[3, 3],[3,5], [2,7], [5,7],[4, 7],可选服务点位置为2，3，5，共3个。
对于第三组测试数据，D=[0,0,0,0]时,所有区间为自身，需在每个节点设服务点，共4个。
@Author      ：Hello World
@Date        ：2025/8/27 下午8:05
"""


# 解题思路：
# 重新理解题目：每个节点必须能够访问到至少一个服务点
# 节点i可以通过最多di条链路来访问服务点
# 需要找到最少数量的服务点，使得所有节点都能访问到至少一个服务点
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
    print("can_reach:", can_reach)
    # 使用贪心算法：每次选择能被最多未覆盖节点访问到的位置
    covered = set()  # 已经被覆盖的节点
    service_points = 0
    print("covered:", covered)
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
        print("best_pos:", best_pos)
        print("best_coverage:", best_coverage)
        # 选择这个位置作为服务点
        service_points += 1
        covered.update(best_coverage)

    return service_points


def submit():
    # 测试模式：自动运行多组示例
    print("=== 测试模式 ===")
    test_cases = [
        (7, [4, 0, 0, 1, 3, 1, 3]),  # 期望输出: 3
        (5, [0, 1, 1, 1, 0]),  # 期望输出: 3
        (4, [0, 0, 0, 0]),  # 期望输出: 4
        (6, [2, 1, 0, 1, 2, 0]),  # 期望输出: 2
        (8, [1, 1, 1, 1, 1, 1, 1, 1]),  # 期望输出: 3
        (3, [0, 0, 0]),  # 期望输出: 3
        (5, [2, 0, 0, 0, 2]),  # 期望输出: 3
    ]

    for i, (n, d) in enumerate(test_cases):
        result = solve(n, d)
        print(f"测试用例 {i+1}: n={n}, d={d}")
        print(f"结果: {result}")
        print(f"期望: {[3, 3, 4, 2, 3, 3, 3][i]}")
        print(f"正确: {'正确' if result == [3, 3, 4, 2, 3, 3, 3][i] else '错误'}")
        print("-" * 50)

    print("\n=== 手动输入模式 ===")
    print("请输入测试数据（按Ctrl+C退出）:")

    try:
        T = int(input())
        for i in range(T):
            n = int(input())
            d = list(map(int, input().split()))
            print(solve(n, d))
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"输入错误: {e}")


submit()
