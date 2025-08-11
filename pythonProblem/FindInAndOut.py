'''
4
0 2 0 3
2 0 3 1
0 3 0 4
3 1 4 0
1 0 1 0
0 2
'''
import heapq

def main():
    # 读取景点数量
    n = int(input())
    dist = []
    # 读取距离矩阵（处理可能包含空格的情况）
    dist = [list(map(int, input().split())) for _ in range(n)]
    # for _ in range(n):
    #     row = input().strip()
    #     # 移除空格,转换为数字列表
    #     dist.append([int(c) for c in row if c != ' '])
    print(dist)
    # 读取出口信息
    exits = input().split()

    # 读取起点和终点
    start_end = input().split()
    start = int(start_end[0])
    end = int(start_end[1])

    # 构建邻接表
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if dist[i][j] > 0:
                graph[i].append((j, dist[i][j]))
    print(graph)
    # Dijkstra算法
    heap = [(0, start, [start])]
    seen = {}

    while heap:
        d, u, path = heapq.heappop(heap)
        if u == end:
            print(' '.join(map(str, path)))
            return
        if u in seen and seen[u] < d:
            continue
        seen[u] = d
        for v, w in graph[u]:
            if v not in seen or d + w < seen.get(v, float('inf')):
                heapq.heappush(heap, (d + w, v, path + [v]))


if __name__ == "__main__":
    main()