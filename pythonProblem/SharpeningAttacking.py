#
# 我们需要设计一个算法来判断游戏角色能否在给定的法力值限制下消灭所有怪物。角色拥有两个技能：
# 刀扇（Fan of Knives）：消耗2点法力，对所有存活怪物造成1点群体伤害。
# 磨刀（Sharpen Blade）：消耗1点法力，伤害翻倍随后选择一个未被磨刀过的怪物造成伤害（初始1点，后续2、4、8...）。
# 输入包含T组测试数据，每组给出怪物数量n、初始法力值m以及每个怪物的血量列表。
# 要求对每组数据判断是否能通过合理使用技能在法力耗尽前消灭所有怪物，输出"Yes"或"No"。
# 输入：
'''
2
4 4
4 6 8 4
4 2
1 2 1 1
'''


# 输出：
# Yes # 第一组可以用2次刀扇消灭所有怪物
# No # 第二组法力不足（需2次刀扇但只有2法力，消灭后剩1血怪物）
def solve():
    t = int(input())  # 读取测试用例数量
    res = []
    for _ in range(t):
        # 读取每组测试数据
        n, m = map(int, input().split())  # 怪物数量和法力值
        a = list(map(int, input().split()))  # 怪物血量列表

        a.sort(reverse=True)  # 将血量降序排列，优先处理高血量怪物

        possible = False  # 标记是否可以消灭所有怪物
        max_k = min(n, m)  # 最大可能的磨刀次数（不能超过怪物数量和法力值）

        # 枚举磨刀次数 k（0到max_k次）
        for k in range(max_k + 1):
            remaining = m - k  # 剩余法力值（总法力减去磨刀消耗）
            if remaining < 0:
                continue  # 法力不足，跳过

            s_max = remaining // 2  # 最大刀扇次数（每次刀扇消耗2法力）
            s_total = s_max * (2 ** k)  # 刀扇总伤害（每次刀扇伤害随磨刀次数翻倍）

            # 检查未被磨刀的怪物（后n-k个）是否能被刀扇消灭
            valid = True
            for i in range(k, n):
                if a[i] > s_total:
                    valid = False
                    break
            if not valid:
                continue  # 存在无法被刀扇消灭的怪物，跳过

            # 检查被磨刀的怪物（前k个）是否能被消灭
            all_ok = True
            for i in range(k):
                j = k - i  # 磨刀顺序（从后往前）
                required = (2 ** j) + s_total  # 所需总伤害（磨刀伤害 + 刀扇伤害）
                if a[i] > required:
                    all_ok = False
                    break
            if all_ok:
                possible = True
                break  # 找到可行方案，退出循环
        res.append("Yes" if possible else "No")
        # print("\nYes" if possible else "No")  # 输出结果
    print('\n'.join(res))
if __name__ == "__main__":
    solve()