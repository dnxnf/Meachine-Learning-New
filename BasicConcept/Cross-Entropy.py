#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：Cross-Entropy.py
@Description ：交叉熵损失函数
@Author      ：Hello World
@Date        ：2025/6/19 上午9:56 
'''
from sklearn.metrics import log_loss

y_true = [0, 1, 1, 0, 1, 1]  # 真实标签
y_pred = [0.1, 0.9, 0.8, 0.3, 0.7, 0.9]  # 预测标签

loss = log_loss(y_true, y_pred)
print("Cross-Entropy loss:", loss)
