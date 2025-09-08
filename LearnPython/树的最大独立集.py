#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：树的最大独立集.py
@Description ：
@Author      ：Hello World
@Date        ：2025/9/8 下午8:03 
'''
# 这个算法通过DFS后序遍历，从叶子节点开始向上计算，
# 确保在计算每个节点时，其所有子节点的状态都已经计算完成。
def max_independent_set_tree(n, edges):
    """
    计算树的最大独立集大小

    参数:
    n: 节点数量
    edges: 边列表

    返回: 最大独立集的大小
    """
    # 构建树
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 使用二维DP数组：dp[u][0] 表示不选节点u，dp[u][1] 表示选节点u
    dp = [[0, 0] for _ in range(n + 1)]

    # DFS遍历
    def dfs(u, parent):
        dp[u][1] = 1  # 选择当前节点
        dp[u][0] = 0  # 不选择当前节点

        for v in graph[u]:
            if v == parent:
                continue
            # 因为是递归， 所以其实是后续遍历
            dfs(v, u)
            # 状态转移
            dp[u][1] += dp[v][0]  # 选u就不能选子节点
            dp[u][0] += max(dp[v][0], dp[v][1])  # 不选u，子节点可选可不选

    # 从根节点开始
    dfs(1, 0)
    return max(dp[1][0], dp[1][1])


def max_independent_set_tree_explained(n, edges):
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 定义更清晰的状态名
    not_choose = [0] * (n + 1)  # 不选该节点时的最大独立集
    choose = [0] * (n + 1)  # 选该节点时的最大独立集

    def dfs(node, parent):
        # 基本情况：当前节点本身
        choose[node] = 1  # 如果选择当前节点，至少包含自己

        # 处理每个子节点
        for child in graph[node]:
            if child == parent:
                continue

            dfs(child, node)  # 先处理子节点

            # 关键逻辑：
            # 1. 如果选择当前节点，就不能选择任何子节点
            choose[node] += not_choose[child]

            # 2. 如果不选择当前节点，可以自由选择每个子节点的最优方案
            not_choose[node] += max(not_choose[child], choose[child])

    dfs(1, 0)

    # 最终结果：根节点选或不选的最大值
    return max(not_choose[1], choose[1])


# 测试示例
if __name__ == "__main__":
    # 示例树：
    #     1
    #    / \
    #   2   3
    #  / \
    # 4   5
    n = 5
    edges = [(1, 2), (1, 3), (2, 4), (2, 5)]

    result = max_independent_set_tree(n, edges)
    ans = max_independent_set_tree_explained(n, edges)
    print("ans: ",ans)
    print(f"最大独立集大小: {result}")  # 输出: 3 (选择节点1,4,5 或 选择节点3,4,5)