#!/usr/bin/env python

# eg: flower flow flight
# dog racecar car
def main():
    strs = list(map(str, input().split()))
    str1 = ""
    flag = 1
    # 一个字符串的大小
    length = len(strs[0])
    # 看每个都一样就加1,需要个标记
    for i in range(length):
        for j in range(1, len(strs)):
            flag = 1
            if strs[0][i] != strs[j][i]:
                flag = 0
                break
        # 没有相等的，结束，输出空白
        if flag == 0:
            break
        elif flag == 1:
            str1 += strs[0][i]
    print(str1)
    pass


if __name__ == "__main__":
    main()
