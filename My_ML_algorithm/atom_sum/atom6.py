#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：atom6.py
@Description ：单原子,F,CI,Br,I
@Author      ：Hello World
@Date        ：2025/6/6 下午5:32 
'''
import numpy as np

# 自变量 x1, x2 和因变量 y
x1 = np.array([3.98, 3.16, 2.96, 2.66])
x2 = np.array([1.58, 1.62, 1.64, 1.64])
y = np.array([1.26, 1.39, 1.42, 1.46])
# 构造设计矩阵
A = np.column_stack([x1, x2, np.ones(len(x1))])

# 最小二乘法求解
coeffs, residuals, _, _ = np.linalg.lstsq(A, y, rcond=None)
a, b, c = coeffs

print(f"多元线性模型: y = {a:.3f} * x1 + {b:.3f} * x2 + {c:.3f}")
# 构造多项式特征
A_poly = np.column_stack([
    x1**2, x2**2, x1*x2, x1, x2, np.ones(len(x1))
])

# 最小二乘法求解
coeffs_poly, *_ = np.linalg.lstsq(A_poly, y, rcond=None)
a_p, b_p, c_p, d_p, e_p, f_p = coeffs_poly

print(f"二次多项式模型:y = {a_p:.3f}x1^2 + {b_p:.3f}x2^2 + {c_p:.3f}x1x2 + {d_p:.3f}x1 + {e_p:.3f}x2 + {f_p:.3f}")
print()