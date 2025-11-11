#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：softmax.py
@Description ：多分类的公式，并用代码实现
@Author      ：Hello World
@Date        ：2025/10/16 下午1:44 
'''

import numpy as np


def softmax(x):
    """Compute softmax values for each sample (row-wise)."""
    # 为数值稳定性，减去每行最大值
    x = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


def run():
    # 每行是一个样本的 logits（3个类别）
    X = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9],
                  [10, 11, 12],
                  [13, 14, 15],
                  [16, 17, 18]], dtype=np.float32)
    print("Softmax output (row-wise):")
    print(softmax(X))


if __name__ == '__main__':
    run()