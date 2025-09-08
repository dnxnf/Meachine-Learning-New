#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：RandomForest.py
@Description ：使用随机森林实现二分类
@Author      ：Hello World
@Date        ：2025/9/8 上午9:27 
'''
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


def use_RandomForest(train, test):
    """
    随机森林算法
    """
    train = np.array(train)
    test = np.array(test)
    # 分离特征和标签
    X_train, y_train = train[:, :-1], train[:, -1]
    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(test)
    # 处理完数据，该模型了
    model = RandomForestClassifier(
        n_estimators=50,
        # max_depth=5,
        random_state=42,
        min_samples_split=2,
        min_samples_leaf=1,
        )
    # 划分训练集和测试集
    model.fit(X_train_scaled, y_train)
    # 预测,astype(int)将结果转化为int型,否则是（1.,0.）
    y_pred = model.predict(X_test_scaled).astype(int)
    # 计算准确率
    return y_pred

def commit():
    train_example = [
        [1.0, 2.0, 0],
        [2.0, 3.0, 1],
        [3.0, 4.0, 0],
        [4.0, 5.0, 1]
    ]

    test_example = [
        [1.5, 2.5],
        [3.5, 4.5]
    ]

    # 进行预测
    result = use_RandomForest(train_example, test_example)
    print("预测结果:", result)
commit()