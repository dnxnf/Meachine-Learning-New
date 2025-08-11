#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：DecisionTree.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/6 上午11:02 
'''
import numpy as np
import math
from collections import Counter


class DecisionTreeNode:
    def __init__(self, feature=None, threshold=None, value=None, left=None, right=None):
        self.feature = feature  # 用于分割的特征索引
        self.threshold = threshold  # 分割阈值(对于连续特征)
        self.value = value  # 叶节点的预测值
        self.left = left  # 左子树
        self.right = right  # 右子树
        self.children = {}  # 子节点(对于离散特征)

    def is_leaf(self):
        return self.value is not None


class DecisionTree:
    def __init__(self, algorithm='id3', max_depth=None, min_samples_split=2):
        self.algorithm = algorithm  # 'id3' 或 'c4.5'
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def fit(self, X, y):
        self.n_classes = len(np.unique(y))
        self.n_features = X.shape[1]
        self.root = self._grow_tree(X, y)

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        # 停止条件
        if (self.max_depth is not None and depth >= self.max_depth) or \
                n_labels == 1 or \
                n_samples < self.min_samples_split:
            leaf_value = self._most_common_label(y)
            return DecisionTreeNode(value=leaf_value)

        # 选择最佳分割特征
        best_feat, best_threshold = self._best_split(X, y)

        if best_feat is None:
            leaf_value = self._most_common_label(y)
            return DecisionTreeNode(value=leaf_value)

        # 分割数据
        if best_threshold is not None:  # 连续特征
            left_idxs = X[:, best_feat] <= best_threshold
            right_idxs = X[:, best_feat] > best_threshold
            left = self._grow_tree(X[left_idxs], y[left_idxs], depth + 1)
            right = self._grow_tree(X[right_idxs], y[right_idxs], depth + 1)
            return DecisionTreeNode(feature=best_feat, threshold=best_threshold, left=left, right=right)
        else:  # 离散特征
            node = DecisionTreeNode(feature=best_feat)
            unique_values = np.unique(X[:, best_feat])
            for value in unique_values:
                subset_idxs = X[:, best_feat] == value
                node.children[value] = self._grow_tree(X[subset_idxs], y[subset_idxs], depth + 1)
            return node

    def _best_split(self, X, y):
        best_gain = -1
        best_feat = None
        best_threshold = None

        for feat_idx in range(self.n_features):
            if len(np.unique(X[:, feat_idx])) == 1:
                continue  # 跳过只有一个取值的特征

            if self.algorithm == 'id3':
                gain = self._information_gain(X[:, feat_idx], y, is_discrete=True)
            else:  # c4.5
                gain = self._gain_ratio(X[:, feat_idx], y)

            if gain > best_gain:
                best_gain = gain
                best_feat = feat_idx
                best_threshold = None  # 对于ID3和C4.5，我们主要处理离散特征

        return best_feat, best_threshold

    def _information_gain(self, X_feat, y, is_discrete=True):
        # 计算信息增益(ID3)
        parent_entropy = self._entropy(y)

        if is_discrete:
            # 离散特征
            unique_values = np.unique(X_feat)
            children_entropy = 0
            for value in unique_values:
                subset_idxs = X_feat == value
                subset_y = y[subset_idxs]
                prob = len(subset_y) / len(y)
                children_entropy += prob * self._entropy(subset_y)
        else:
            # 连续特征(这里简化处理)
            pass

        return parent_entropy - children_entropy

    def _gain_ratio(self, X_feat, y):
        # 计算增益率(C4.5)
        information_gain = self._information_gain(X_feat, y)
        split_info = self._split_information(X_feat)

        if split_info == 0:
            return 0  # 避免除以0

        return information_gain / split_info

    def _split_information(self, X_feat):
        # 计算分裂信息(用于增益率分母)
        _, counts = np.unique(X_feat, return_counts=True)
        probs = counts / len(X_feat)
        return -np.sum([p * np.log2(p) for p in probs if p > 0])

    def _entropy(self, y):
        # 计算熵
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log2(p) for p in ps if p > 0])

    def _most_common_label(self, y):
        counter = Counter(y)
        return counter.most_common(1)[0][0]

    def _traverse_tree(self, x, node):
        if node.is_leaf():
            return node.value

        if node.threshold is not None:  # 连续特征
            if x[node.feature] <= node.threshold:
                return self._traverse_tree(x, node.left)
            else:
                return self._traverse_tree(x, node.right)
        else:  # 离散特征
            value = x[node.feature]
            if value in node.children:
                return self._traverse_tree(x, node.children[value])
            else:
                return self._most_common_label(y)  # 处理未知值


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 加载数据集
iris = load_iris()
X, y = iris.data, iris.target

# 添加一些离散特征用于演示
discrete_feat = np.random.choice(['a', 'b', 'c'], size=len(X))
X = np.column_stack((X, discrete_feat))

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ID3决策树
id3_tree = DecisionTree(algorithm='id3', max_depth=3)
id3_tree.fit(X_train, y_train)
id3_pred = id3_tree.predict(X_test)
print(f"ID3 Accuracy: {accuracy_score(y_test, id3_pred):.4f}")

# C4.5决策树
c45_tree = DecisionTree(algorithm='c4.5', max_depth=3)
c45_tree.fit(X_train, y_train)
c45_pred = c45_tree.predict(X_test)
print(f"C4.5 Accuracy: {accuracy_score(y_test, c45_pred):.4f}")
