def dfs(i, j, count, out):
    # 如果到了边界、遇到了X或已经在连通域中，则直接返回结果。
    if i < 0 or i >= m or j < 0 or j >= n \
            or areas[i][j] == "X" or (i, j) in checked:
        return count

    checked.add((i, j))
    # 当遇到入口时，则加入到结果列表中
    if i == 0 or i == m - 1 or j == 0 or j == n - 1:
        out.append((i, j))

    count += 1
    # 继续对各个方向进行深度优先搜索
    for offsetX, offsetY in directions:
        newI = i + offsetX
        newJ = j + offsetY
        count = dfs(newI, newJ, count, out)

    return count


def solve_method(areas):
    global checked, m, n, directions
    m = len(areas)
    n = len(areas[0])
    checked = set()
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    candidates = []  # 存储所有单入口区域 (entry_i, entry_j, size)

    for i in range(m):
        for j in range(n):
            if areas[i][j] == "O" and (i, j) not in checked:
                out = []  # 存储边界入口点
                count = dfs(i, j, 0, out)

                # 只有恰好一个入口的区域才考虑
                if len(out) == 1:
                    entry_i, entry_j = out[0]
                    candidates.append((entry_i, entry_j, count))

    # 处理结果
    if not candidates:
        return "NULL"
    elif len(candidates) == 1:
        return candidates[0]  # 返回 (i, j, count)
    else:
        # 找到最大的区域
        max_size = max(candidate[2] for candidate in candidates)
        # 找出所有最大大小的区域
        max_candidates = [c for c in candidates if c[2] == max_size]

        if len(max_candidates) == 1:
            return max_candidates[0]  # 返回最大的单入口区域
        else:
            # 如果有多个相同大小的最大区域，返回大小值
            return max_size


if __name__ == '__main__':
    # 测试用例1：单入口区域
    areas = [["X", "X", "X", "X"],
             ["X", "O", "O", "X"],
             ["X", "O", "O", "X"],
             ["X", "O", "X", "X"]]
    result = solve_method(areas)
    print(f"测试1: {result}")  # 应该是 (3, 1, 5)
    assert result == (3, 1, 5)

    # 测试用例2：单入口小区域
    areas = [["X", "X", "X", "X", "X"],
             ["O", "O", "O", "O", "X"],
             ["X", "O", "O", "O", "X"],
             ["X", "O", "X", "X", "O"]]
    result = solve_method(areas)
    print(f"测试2: {result}")  # 应该是 (3, 4, 1)
    assert result == (3, 4, 1)

    # 测试用例3：无单入口区域
    areas = [["X", "X", "X", "X"],
             ["X", "O", "O", "O"],
             ["X", "O", "O", "O"],
             ["X", "O", "O", "X"],
             ["X", "X", "X", "X"]]
    result = solve_method(areas)
    print(f"测试3: {result}")  # 应该是 "NULL"
    assert result == "NULL"

    # 测试用例4：多个单入口区域
    areas = [["X", "X", "X", "X"],
             ["X", "O", "O", "O"],
             ["X", "X", "X", "X"],
             ["X", "O", "O", "O"],
             ["X", "X", "X", "X"]]
    result = solve_method(areas)
    print(f"测试4: {result}")  # 应该是 3 (两个区域大小都是3)
    assert result == 3