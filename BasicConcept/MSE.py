#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：MSE.py
@Description ：MSE(Mean Squared Error)，均方误差
@Author      ：Hello World
@Date        ：2025/6/19 上午9:48 
'''
#使用sklearn包实现
from sklearn.metrics import mean_squared_error

y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]
# 均方误差直接调用函数即可，真实值在前，预测值在后
# 公式：MSE = 1/n * sum((y_true - y_pred)^2)
mse = mean_squared_error(y_true, y_pred)
print("MSE:", mse)
