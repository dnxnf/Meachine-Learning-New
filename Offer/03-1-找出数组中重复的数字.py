'''
题目：
在一个长度为n的数组里有所有数字都在0~n-1的范围内，数组中某些数字是重复的，但不知道有几个数字重复了，
也不知道每个数字重复了几次，请找出数组中任意一个重复的数字，例如，如果输入长度为7的数组 [ 2, 3, 1, 0, 2, 5, 3 ] ，
那么对应的输出是重复的数字2或者3。

对原数组进行排序然后顺序查找，时间 O(nlogn) 空间 O(1)
利用哈希表解决，无需修改原数组，时间 O(n) 空间 O(n)
交换原数组中的元素，时间 O(n) 空间 O(1)
第三种方法最优，以下是实现
'''


def duplicate(arr):
    # 检查输入是否为列表
    if not isinstance(arr, list):
        return -1

    length = len(arr)

    # 验证数组中的每个元素
    for i in range(length):
        # 检查元素是否为整数
        if not isinstance(arr[i], int):
            return -1
        # 检查元素值是否在有效范围内 (0 到 length-1)
        if arr[i] < 0 or arr[i] > length - 1:
            return -1

    # 查找重复数字的核心算法
    for i in range(length):
        # 当元素不在其"正确"位置时进行交换
        while arr[i] != i:
            # 如果发现重复
            if arr[i] == arr[arr[i]]: # 当前元素和正确位置元素相同
                return arr[i]
            # 交换元素到其"正确"位置
            temp = arr[i]
            arr[i], arr[temp] = arr[temp], arr[i]

    # 如果没有找到重复，返回-1
    return -1


# 测试用例
# 长度为 n 的数组里包含一个或多个重复的数字
test_case1 = [2, 3, 1, 0, 2, 5, 3]

# 数组中不含重复的数字
test_case2 = [2, 3, 1, 5, 4, 0]

# 无效输入测试用例
test_case3 = None
test_case4 = [2, 6, 1, 0]

print("test case1:", duplicate(test_case1))
print("test case2:", duplicate(test_case2))
print("test case3:", duplicate(test_case3))
print("test case4:", duplicate(test_case4))
