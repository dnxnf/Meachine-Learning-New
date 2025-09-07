#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：KNN.py
@Description ：分类，其类型等于离自身最近的k的邻居的类别
@Author      ：Hello World
@Date        ：2025/8/30 下午2:50 
'''
from collections import Counter

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


class KNN:
    def __init__(self, k):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        """预测新数据点的类别"""
        predictions = [self._predict(x) for x in X]
        return np.array(predictions)

    def _predict(self, x):
        """给定单个数据点x，返回其类别"""
        distances = [self.distance(x, x_train) for x_train in self.X_train]
        K_indices = np.argsort(distances)[:self.k]
        k_nearest_y = [self.y_train[i] for i in K_indices]
        most_common_y = max(set(k_nearest_y), key=k_nearest_y.count)
        return most_common_y

    def distance(self, x1, x2):
        """计算两个数据点之间的距离"""
        return np.sqrt(np.sum((x1 - x2) ** 2))


def sample_test(X_train, y_train, X_test, k=3):
    knn = KNN(k=3)
    knn.fit(X_train, y_train)
    y_test = knn.predict(X_test)
    print(y_test)


def iris_test():
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    knn = KNN(k=3)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    print('y_pred:', y_pred)
    print("y_test:", y_test)


def KNN2(X_train, y_train, X_test, X_test_label=None, k=3):
    '''
    :param X_train: 训练集特征数据 (n_samples, n_features)
    :param y_train: 训练集标签数据 (n_samples,)
    :param X_test: 测试集特征数据 (n_samples, n_features)
    :param X_test_label: 测试集标签数据 (n_samples,)，如果为None则不与预测的比较，只返回预测的标签数据
    :param k: kNN算法参数，默认为3
    :return:预测的标签数据 (n_samples,)
    '''
    predictions = []

    def get_distance(x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))

    for i in range(len(X_test)):  # 遍历测试集
        distances = []
        for j in range(len(X_train)):  # 对于每个测试集数据，遍历训练集
            dist = get_distance(X_test[i], X_train[j])
            distances.append((dist, y_train[j]))
        distances.sort(key=lambda x: x[0])  # 找到距离最小的k个点
        k_nearest_y = distances[:k]  # 得到k个点的标签
        most_common_y = Counter(k_nearest_y).most_common(1)[0][0][1]  # 得到出现次数最多的标签
        predictions.append(most_common_y)  # 预测标签加入列表
    if X_test_label is None:
        return np.array(predictions)
    # np.array会自动将列表转换为数组
    else:
        return np.array(predictions), X_test_label


def KNN2_optimized(X_train, y_train, X_test, X_test_label=None, k=3):
    """
    优化版的KNN实现，使用向量化操作提高效率
    """
    predictions = []

    for test_sample in X_test:
        # 向量化计算距离（避免内层循环）
        distances = np.sqrt(np.sum((X_train - test_sample) ** 2, axis=1))
        # 广播，得到一个兼容的矩阵(n_train,test_sample),也就是(10,2)
        # 所以可以和每一个都直接算距离,axis=1求和（对每行求和），再开方

        k_indices = np.argsort(distances)[:k]
        # print(k_indices)
        # 获取对应的标签
        k_nearest_labels = y_train[k_indices]
        print(k_nearest_labels)
        # 统计最常见的标签
        most_common = Counter(k_nearest_labels).most_common(1)[0][0]
        predictions.append(most_common)

    predictions = np.array(predictions)

    if X_test_label is None:
        return predictions
    else:
        return predictions, X_test_label


def knn3(X_train, y_train, X_test, X_test_label=None, k=3):
    def getdistance(x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))
    predictions = []
    for i in range(len(X_test)):
        distances = []
        for j in range(len(X_train)):
            dist = getdistance(X_test[i], X_train[j])
            distances.append((dist, y_train[j])) # 距离和标签的组合
        distances.sort(key=lambda x: x[0])
        k_nearest_y = distances[:k]
        k_nearest_labels = [x[1] for x in k_nearest_y]
        most_common_y = Counter(k_nearest_labels).most_common(1)[0][0]
        predictions.append(most_common_y)
    if X_test_label is None:
        return np.array(predictions)
    else:
        return np.array(predictions), X_test_label

if __name__ == '__main__':
    X_train = np.array([[1, 2], [2, 3], [3, 1], [4, 3], [5, 2],
                        [6, 4], [7, 5], [8, 6], [9, 7], [10, 8]])
    y_train = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 1])
    X_test = np.array([[5, 4], [6, 5], [7, 6], [8, 7], [9, 8]])
    knn = KNN(k=3)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    print(y_pred)
    # print(KNN2(X_train, y_train, X_test, k=3))
    # sample_test(X_train, y_train, X_test, k=3)
    # print(KNN2_optimized(X_train, y_train, X_test, k=3))
    print(knn3(X_train, y_train, X_test, k=3))
