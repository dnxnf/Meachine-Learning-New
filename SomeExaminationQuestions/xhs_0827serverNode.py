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
def solve1(n, d):
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

    # 我们可以将问题转化为：选择最少的点，使得每个区间[i - di, i + di]都至少包含一个被选中的点。
    # 这是一个典型的区间覆盖问题，可以用贪心算法解决。
    '''
    预处理区间：对于每个节点 i，计算它能覆盖的区间 [left_i, right_i]
    left_i = max(1, i - di) （节点编号从1开始）
    right_i = min(n, i + di)
    按右端点排序：将所有区间按右端点从小到大排序
    贪心选择：
    初始化：当前覆盖位置 curr_end = 0，服务点数量 count = 0
    遍历排序后的区间：
    如果区间的左端点 > curr_end，说明需要新的服务点
    选择当前区间的右端点作为服务点位置更新 curr_end 为当前服务点能覆盖到的最远位置
    '''


def solve(num, data):
    """
    解决服务器节点部署问题
    参数:
    num: 节点数 n
    data: 每个节点的传输限制列表 [d1, d2, ..., dn]
    返回:
    最少需要部署的服务点数
    要让每个区间都有服务点，按照右端点排序，后面的右端点都大于前面的右端点，
    将每个服务点部署到右端点，然后比较后面的和前面的左端点，左端点能在已部署的服务点的右端点之前，则不用管
    """
    n = num  # 节点数

    # 为每个节点创建覆盖区间 [left, right]
    intervals = []
    for i in range(1, n + 1):
        di = data[i - 1]  # 第i个节点的传输限制
        # 计算节点i能覆盖的左边界：max(1, i - di) 确保不小于1（节点编号从1开始）
        left = max(1, i - di)
        # 计算节点i能覆盖的右边界：min(n, i + di) 确保不大于n
        right = min(n, i + di)
        intervals.append((left, right))

    # 关键步骤：按区间的右端点进行升序排序
    # 这样我们可以优先处理结束较早的区间，使用贪心策略选择服务点
    intervals.sort(key=lambda x: x[1])
    print(intervals)
    count = 0  # 记录需要的服务点数量
    curr_end = 0  # 当前已覆盖到的最远位置（初始为0，表示还没覆盖任何节点）

    # 遍历所有排序后的区间
    for left, right in intervals:
        # 如果当前区间的左端点大于已覆盖的最远位置
        # 说明这个区间还没有被覆盖，需要新的服务点
        if left > curr_end:
            count += 1  # 增加服务点数量
            curr_end = right  # 在当前区间的右端点部署服务点
            # 在右端点部署可以覆盖尽可能多的后续区间

    return count


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
        print(f"测试用例 {i + 1}: n={n}, d={d}")
        print(f"结果: {result}")
        print(f"期望: {[3, 3, 4, 2, 3, 3, 3][i]}")
        print('正确' if result == [3, 3, 4, 2, 3, 3, 3][i] else '错误')
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
