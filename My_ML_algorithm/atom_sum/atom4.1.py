#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：atom4.1.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/6 下午5:13 
'''
import numpy as np
from scipy.optimize import curve_fit

# 定义模型函数
def model(X, k, c1, c2):
    x, C_sum, H_sum = X
    y1 = 7.53 * np.exp(-0.82 * x + c1)
    y2 = -0.0259 * C_sum + 0.0223 * H_sum + c2
    return k * y1 * y2

# 输入数据
x_data = np.array([3, 3, 2])
C_sum_data = np.array([7.65, 5.1, 2.55])
H_sum_data = np.array([0, 2.2, 2.2])
Y_observed = np.array([0.66, 0.72, 1.25])

# 拟合模型
popt, _ = curve_fit(model, (x_data, C_sum_data, H_sum_data), Y_observed)

# 拟合后的参数
k_fit, c1_fit, c2_fit = popt
print("拟合结果：")
print(f"k = {k_fit}")
print(f"c1 = {c1_fit}")
print(f"c2 = {c2_fit}")