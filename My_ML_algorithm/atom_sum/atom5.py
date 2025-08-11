#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：atom5.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/6 下午5:28 
'''
import numpy as np

# 数据
x = np.array([5, 4, 3])
y = np.array([0.68, 0.75, 1.04])

# 最小二乘法拟合线性模型
A = np.vstack([x, np.ones(len(x))]).T
a, b = np.linalg.lstsq(A, y, rcond=None)[0]

print(f"线性模型: y = {a:.3f}x + {b:.3f}")