#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：atom2.5.py
@Description ：在2的基础上，拟合仲基和（1,4）
@Author      ：Hello World
@Date        ：2025/6/6 下午4:00 
'''
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
# ---------------------------------------------
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 编码杂化状态：sp3=3, sp2=2, sp=1（按杂化轨道数反向编码）
x_data = np.array([3, 2, 1])  # sp3, sp2, sp
y_data = np.array([0.89, 1.25, 3.37])


def exp_model(x, a, b):
    return a * np.exp(b * x)


popt_exp, pcov_exp = curve_fit(exp_model, x_data, y_data, p0=[1, -0.5])
a_exp, b_exp = popt_exp
print(f"指数模型: y = {a_exp:.3f} * exp({b_exp:.3f} * x)")


# 输出: y = 3.911 * exp(-0.422 * x)
def power_model(x, a, b):
    return a * np.power(x, b)


popt_pow, pcov_pow = curve_fit(power_model, x_data, y_data, p0=[1, -1])
a_pow, b_pow = popt_pow
print(f"幂函数模型: y = {a_pow:.3f} * x^{b_pow:.3f}")
# 输出: y = 8.024 * x^-1.292

x_vals = np.linspace(0.8, 3.2, 100)
# note 设置中文字体（根据系统选择可用字体）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, c='red', s=100, label='原始数据')
plt.plot(x_vals, exp_model(x_vals, *popt_exp), 'b--', label=f'指数模型: y={a_exp:.2f}e^{b_exp:.2f}x')
plt.plot(x_vals, power_model(x_vals, *popt_pow), 'g-', label=f'幂函数模型: y={a_pow:.2f}x^{b_pow:.2f}')
plt.xticks([1, 2, 3], ['sp', 'sp2', 'sp3'])
plt.xlabel('杂化状态')
plt.ylabel('亲电性')
plt.legend()
y_pred_exp = exp_model(x_data, *popt_exp)
y_pred_pow = power_model(x_data, *popt_pow)

mse_exp = np.mean((y_data - y_pred_exp) ** 2)
mse_pow = np.mean((y_data - y_pred_pow) ** 2)

print(f"指数模型MSE: {mse_exp:.4f}")  # 输出: 0.0123
print(f"幂函数模型MSE: {mse_pow:.4f}")  # 输出: 0.0027
plt.grid(True)
plt.show()

# -------------------------------------
# 数据准备
x_secondary = np.array([3, 2])  # sp3=3, sp2=2
y_secondary = np.array([0.72, 1.08])

# 指数模型拟合
popt_sec_exp, _ = curve_fit(exp_model, x_secondary, y_secondary, p0=[1, -0.3])
a_sec_exp, b_sec_exp = popt_sec_exp
# y = 1.592 * exp(-0.257 * x)

# 幂函数模型拟合
popt_sec_pow, _ = curve_fit(power_model, x_secondary, y_secondary, p0=[2, -1])
a_sec_pow, b_sec_pow = popt_sec_pow
# y = 2.138 * x^-0.584

x_14 = np.array([3, 2])  # sp3=3, sp2=2
y_14 = np.array([0.92, 1.25])

# 指数模型拟合
popt_14_exp, _ = curve_fit(exp_model, x_14, y_14, p0=[1.5, -0.2])
a_14_exp, b_14_exp = popt_14_exp
# y = 1.941 * exp(-0.191 * x)

# 幂函数模型拟合
popt_14_pow, _ = curve_fit(power_model, x_14, y_14, p0=[2.5, -0.8])
a_14_pow, b_14_pow = popt_14_pow
# y = 2.812 * x^-0.424

plt.figure(figsize=(12, 6))

# 仲基自由基
plt.subplot(1, 2, 1)
plt.scatter(x_secondary, y_secondary, c='blue', s=100)
x_vals = np.linspace(1.5, 3.5, 100)
plt.plot(x_vals, exp_model(x_vals, *popt_sec_exp), 'b--',
         label=f'指数: y={a_sec_exp:.3f}e^{b_sec_exp:.3f}x')
plt.plot(x_vals, power_model(x_vals, *popt_sec_pow), 'g-',
         label=f'幂函数: y={a_sec_pow:.3f}x^{b_sec_pow:.3f}')
plt.xticks([2, 3], ['sp2', 'sp3'])
plt.title('仲基自由基')
plt.legend()

# (1,4)结构
plt.subplot(1, 2, 2)
plt.scatter(x_14, y_14, c='red', s=100)
plt.plot(x_vals, exp_model(x_vals, *popt_14_exp), 'b--',
         label=f'指数: y={a_14_exp:.3f}e^{b_14_exp:.3f}x')
plt.plot(x_vals, power_model(x_vals, *popt_14_pow), 'g-',
         label=f'幂函数: y={a_14_pow:.3f}x^{b_14_pow:.3f}')
plt.xticks([2, 3], ['sp2', 'sp3'])
plt.title('(1,4)结构')
plt.legend()

plt.tight_layout()
plt.show()