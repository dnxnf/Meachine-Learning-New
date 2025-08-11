#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：28RectangleArea.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午8:26
题目描述
给出3组点坐标(x,y,w,h)，-1000<x,y<1000，w,h为正整数。
(x,y,w,h)表示平面直角坐标系中的一个矩形:
x,y为矩形左上角坐标点，w,h向右w，向下h。
(x,y,w,h)表示x轴(x,x+w)和y轴(y,y-h)围成的矩形区域
(0,0,2,2)表示00,20,0-2,2-2围成的矩形区域:
(3,5,4,6)表示x轴方向(3,7)和y方向(5,-1)围成的矩形区域
求3组坐标构成的矩形区域重合部分的面积。
输入描述
3行输入分别为3个矩形的位置，分别代表“左上角x坐标”“左上角y坐标”"矩形宽”
"矩形高”-1000<=x,y<1000
1 6 4 4
3 5 3 4
0 3 7 3
输出描述:输出3个矩形相交的面积，不相交的输出0.
2
'''


def compute_intersection_area(rectangles):
    if len(rectangles) < 3:
        return 0

    # 初始相交区域设为第一个矩形
    x1, y1, w1, h1 = rectangles[0]
    inter_x_left = x1
    inter_x_right = x1 + w1
    inter_y_top = y1
    inter_y_bottom = y1 - h1

    # 依次与后面的矩形求交集
    for rect in rectangles[1:]:
        x, y, w, h = rect
        current_x_left = x
        current_x_right = x + w
        current_y_top = y
        current_y_bottom = y - h

        # 计算x轴方向的交集
        new_x_left = max(inter_x_left, current_x_left)
        new_x_right = min(inter_x_right, current_x_right)
        if new_x_left >= new_x_right:
            return 0

        # 计算y轴方向的交集
        new_y_top = min(inter_y_top, current_y_top)
        new_y_bottom = max(inter_y_bottom, current_y_bottom)
        if new_y_top <= new_y_bottom:
            return 0

        # 更新交集区域
        inter_x_left, inter_x_right = new_x_left, new_x_right
        inter_y_top, inter_y_bottom = new_y_top, new_y_bottom

    # 计算面积
    width = inter_x_right - inter_x_left
    height = inter_y_top - inter_y_bottom
    area = width * height
    return area


# 读取输入
rectangles = []
for _ in range(3):
    x, y, w, h = map(int, input().split())
    rectangles.append((x, y, w, h))
# print(rectangles)

# 计算并输出结果
print(compute_intersection_area(rectangles))