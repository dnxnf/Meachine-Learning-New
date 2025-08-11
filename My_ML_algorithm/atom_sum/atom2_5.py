#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：atom2_5.py
@Description ：在2的基础上，仅通过加减常数来实现对仲基和（1,4）的拟合，不修改系数值
@Author      ：Hello World
@Date        ：2025/6/6 下午4:14 
'''
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 编码杂化状态：sp3=3, sp2=2, sp=1
x_data = np.array([3, 2, 1])  # sp3, sp2, sp
y_data = np.array([0.89, 1.25, 3.37])

# 仲基自由基数据
x_secondary = np.array([3, 2])  # sp3=3, sp2=2
y_secondary = np.array([0.72, 1.08])

# (1,4)结构数据
x_14 = np.array([3, 2])  # sp3=3, sp2=2
y_14 = np.array([0.92, 1.25])

# 定义带常数项的模型
def exp_model_c(x, a, b, c):
    return a * np.exp(b * x) + c

def power_model_c(x, a, b, c):
    return a * np.power(x, b) + c

# 拟合仲基自由基
try:
    popt_sec_exp, _ = curve_fit(exp_model_c, x_secondary, y_secondary, p0=[1, -0.3, 0])
    a_sec_exp, b_sec_exp, c_sec_exp = popt_sec_exp
    print(f"仲基自由基-指数模型: y = {a_sec_exp:.3f} * exp({b_sec_exp:.3f} * x) + {c_sec_exp:.3f}")
except:
    print("仲基自由基-指数模型拟合失败，使用原始模型")
    popt_sec_exp, _ = curve_fit(exp_model, x_secondary, y_secondary, p0=[1, -0.3])
    a_sec_exp, b_sec_exp = popt_sec_exp
    c_sec_exp = 0

try:
    popt_sec_pow, _ = curve_fit(power_model_c, x_secondary, y_secondary, p0=[2, -1, 0])
    a_sec_pow, b_sec_pow, c_sec_pow = popt_sec_pow
    print(f"仲基自由基-幂函数模型: y = {a_sec_pow:.3f} * x^{b_sec_pow:.3f} + {c_sec_pow:.3f}")
except:
    print("仲基自由基-幂函数模型拟合失败，使用原始模型")
    popt_sec_pow, _ = curve_fit(power_model, x_secondary, y_secondary, p0=[2, -1])
    a_sec_pow, b_sec_pow = popt_sec_pow
    c_sec_pow = 0

# 拟合(1,4)结构
try:
    popt_14_exp, _ = curve_fit(exp_model_c, x_14, y_14, p0=[1.5, -0.2, 0])
    a_14_exp, b_14_exp, c_14_exp = popt_14_exp
    print(f"(1,4)结构-指数模型: y = {a_14_exp:.3f} * exp({b_14_exp:.3f} * x) + {c_14_exp:.3f}")
except:
    print("(1,4)结构-指数模型拟合失败，使用原始模型")
    popt_14_exp, _ = curve_fit(exp_model, x_14, y_14, p0=[1.5, -0.2])
    a_14_exp, b_14_exp = popt_14_exp
    c_14_exp = 0

try:
    popt_14_pow, _ = curve_fit(power_model_c, x_14, y_14, p0=[2.5, -0.8, 0])
    a_14_pow, b_14_pow, c_14_pow = popt_14_pow
    print(f"(1,4)结构-幂函数模型: y = {a_14_pow:.3f} * x^{b_14_pow:.3f} + {c_14_pow:.3f}")
except:
    print("(1,4)结构-幂函数模型拟合失败，使用原始模型")
    popt_14_pow, _ = curve_fit(power_model, x_14, y_14, p0=[2.5, -0.8])
    a_14_pow, b_14_pow = popt_14_pow
    c_14_pow = 0

# 绘图
plt.figure(figsize=(12, 6))

# 仲基自由基
plt.subplot(1, 2, 1)
plt.scatter(x_secondary, y_secondary, c='blue', s=100)
x_vals = np.linspace(1.5, 3.5, 100)
plt.plot(x_vals, exp_model_c(x_vals, *popt_sec_exp), 'b--',
         label=f'指数: y={a_sec_exp:.3f}e^{b_sec_exp:.3f}x+{c_sec_exp:.3f}')
plt.plot(x_vals, power_model_c(x_vals, *popt_sec_pow), 'g-',
         label=f'幂函数: y={a_sec_pow:.3f}x^{b_sec_pow:.3f}+{c_sec_pow:.3f}')
plt.xticks([2, 3], ['sp2', 'sp3'])
plt.title('仲基自由基')
plt.legend()

# (1,4)结构
plt.subplot(1, 2, 2)
plt.scatter(x_14, y_14, c='red', s=100)
plt.plot(x_vals, exp_model_c(x_vals, *popt_14_exp), 'b--',
         label=f'指数: y={a_14_exp:.3f}e^{b_14_exp:.3f}x+{c_14_exp:.3f}')
plt.plot(x_vals, power_model_c(x_vals, *popt_14_pow), 'g-',
         label=f'幂函数: y={a_14_pow:.3f}x^{b_14_pow:.3f}+{c_14_pow:.3f}')
plt.xticks([2, 3], ['sp2', 'sp3'])
plt.title('(1,4)结构')
plt.legend()

plt.tight_layout()
plt.show()
