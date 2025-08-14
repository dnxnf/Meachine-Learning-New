'''
题目：剪绳子
给你一根长度为n的绳子，请把绳子剪成m段（m、n都是整数，n>1,m>1），
每段绳子的长度记为 k[0], k[1], k[2], …, k[m]。
请问 k[0] * k[1] * k[2] * … * k[m] 可能的最大乘积是多少？
例如，当绳子的长度为8时，我们把它剪成长度分别为2、3、3的三段，此时得到的最大乘积是18。
'''


def max_product_after_cutting_solution0(length):
    # 使用动态规划，dp[i]将绳子剪成至少两段的最大乘积
    '''
    对于每个整数 i（从 3 到 n），我们需要考虑所有可能的拆分方式：
    将 i 拆分成 j 和 i - j（其中 1 ≤ j < i）。
    对于每一种拆分方式，有两种选择：
    不继续拆分 i - j，此时乘积为 j * (i - j)。
    继续拆分 i - j，此时乘积为 j * dp[i - j]（因为 dp[i - j] 已经是 i - j 的最大乘积）。
    我们需要取这两种情况的最大值，然后对所有可能的 j 取最大值，即：
    '''
    # 拆分之后可能会继续拆分
    dp = [0 for i in range(length + 1)]
    for i in range(2, length + 1):
        for j in range(i):
            dp[i] = max(dp[i], dp[i - j] * j, j * (i - j))
    return dp[length]


# 动态规划
def max_product_after_cutting_solution1(length):
    if length < 2:
        return 0
    if length == 2:
        return 1
    if length == 3:
        return 2
    products = [0] * (length + 1)
    products[0] = 0
    products[1] = 1
    products[2] = 2
    products[3] = 3
    for i in range(4, length + 1):
        max = 0
        for j in range(1, i // 2 + 1):
            products[i] = products[j] * products[i - j]
            if products[i] > max:
                max = products[i]
        products[i] = max
    return products[length]


# 贪婪算法
def max_product_after_cutting_solution2(length):
    '''

    :param length:
    :return:
基于数学发现：当把一个数拆分成多个3的乘积时，乘积会最大化。具体规则如下：
当n >= 4时，尽可能多地拆分成3

如果最后剩下1，从前面借一个3，变成2+2（因为3+1不如2+2）
    '''
    if length < 2:
        return 0
    if length == 2:
        return 1
    if length == 3:
        return 2
    times_of_3 = length // 3
    if length - times_of_3 * 3 == 1:
        times_of_3 -= 1
    times_of_2 = (length - times_of_3 * 3) / 2
    return (3 ** times_of_3) * (2 ** times_of_2)


print(max_product_after_cutting_solution0(8))
print(max_product_after_cutting_solution1(8))
print(max_product_after_cutting_solution2(8))
