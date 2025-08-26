#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MachineLearning 
@File    ：IsolationForest.py
@IDE     ：PyCharm 
@Author  ：Hello World
@Date    ：2025/5/26 下午5:30 
'''
'''
描述：
孤立森林异常检测算法的输入为包含样本数量、特征数量、样本特征值矩阵以及模型参数（孤立树数量和子样本大小）
的标准化数据流，算法通过构建多棵随机子样本训练的孤立树来评估每个样本的异常程度，输出每个样本的异常分数
（0-1之间的浮点数，值越大表示异常可能性越高）和对应的二进制标签（0表示正常，1表示异常），
从而实现高效、可扩展的异常检测功能。
输入：
5 2
1.0 2.0
1.1 2.1
10.0 20.0
1.2 2.2
10.1 20.1
100 256
输出：
0.1234 0
0.1256 0
0.5678 0
0.1245 0
0.9876 1
'''
import numpy as np
import math
from random import randint, choice


class IsolationTree:
    """孤立树实现，用于隔离异常点"""

    def __init__(self, height_limit):
        self.height_limit = height_limit  # 树的最大高度限制
        self.n_nodes = 0  # 节点计数器
        self.root = None  # 树的根节点

    def fit(self, X: np.ndarray, current_height=0):
        """递归构建孤立树"""
        # 终止条件：达到高度限制或只剩一个样本
        if current_height >= self.height_limit or len(X) <= 1:
            self.n_nodes += 1
            return {"type": "leaf", "size": len(X), "n_nodes": self.n_nodes}

        # 随机选择特征和分割值
        n_features = X.shape[1]
        split_feature = randint(0, n_features - 1)  # 随机选择特征
        min_val = X[:, split_feature].min()
        max_val = X[:, split_feature].max()

        # 如果所有值相同，直接创建叶节点
        if min_val == max_val:
            self.n_nodes += 1
            return {"type": "leaf", "size": len(X), "n_nodes": self.n_nodes}

        split_value = np.random.uniform(min_val, max_val)  # 随机选择分割值

        # 根据分割值划分左右子树
        left_mask = X[:, split_feature] < split_value
        right_mask = ~left_mask

        self.n_nodes += 1
        node = {
            "type": "node",
            "split_feature": split_feature,
            "split_value": split_value,
            "left": None,
            "right": None,
            "n_nodes": self.n_nodes
        }

        # 递归构建左右子树
        node["left"] = self.fit(X[left_mask], current_height + 1)
        node["right"] = self.fit(X[right_mask], current_height + 1)

        # 如果是根节点，保存引用
        if current_height == 0:
            self.root = node

        return node

    def path_length(self, x, node=None):
        """计算样本x在当前树中的路径长度"""
        if node is None:
            node = self.root

        # 到达叶节点，返回调整后的路径长度
        if node["type"] == "leaf":
            if node["size"] == 1:
                return 0
            # 使用修正项c(n)调整路径长度
            return self._c(node["size"])

        # 根据特征值决定走左子树还是右子树
        if x[node["split_feature"]] < node["split_value"]:
            return 1 + self.path_length(x, node["left"])
        else:
            return 1 + self.path_length(x, node["right"])

    def _c(self, n):
        """计算路径长度的修正项"""
        if n <= 1:
            return 0
        # 使用欧拉常数(≈0.5772156649)的修正公式
        return 2 * (math.log(n - 1) + 0.5772156649) - (2 * (n - 1) / n)


class IsolationForest:
    """孤立森林实现，包含多棵孤立树"""

    def __init__(self, n_trees=100, sample_size=256):
        self.n_trees = n_trees  # 树的数量
        self.sample_size = sample_size  # 每棵树的样本大小
        self.trees = []  # 存储所有孤立树
        self.height_limit = None  # 树的高度限制

    def fit(self, X: np.ndarray):
        """训练孤立森林"""
        n_samples = X.shape[0]
        self.sample_size = min(self.sample_size, n_samples)
        # 计算树的高度限制为log2(sample_size)
        self.height_limit = math.ceil(math.log2(self.sample_size))

        # 构建多棵孤立树
        for _ in range(self.n_trees):
            # 随机子采样(无放回)
            sample_indices = np.random.choice(n_samples, self.sample_size, replace=False)
            X_subset = X[sample_indices]

            # 创建并训练孤立树
            tree = IsolationTree(self.height_limit)
            tree.fit(X_subset)
            self.trees.append(tree)

    def anomaly_score(self, X, psi=None):
        """计算样本的异常分数"""
        if psi is None:
            psi = self.sample_size

        scores = []
        for x in X:
            path_lengths = []
            # 计算每棵树中的路径长度
            for tree in self.trees:
                path_length = tree.path_length(x)
                path_lengths.append(path_length)

            # 计算平均路径长度
            avg_path_length = np.mean(path_lengths)
            c = self._c(psi)
            # 计算异常分数(0-1之间，越接近1表示越异常)
            score = 2 ** (-avg_path_length / c)
            scores.append(score)

        return np.array(scores)

    def predict(self, X, threshold=0.5):
        """预测样本是否为异常"""
        scores = self.anomaly_score(X)
        return (scores > threshold).astype(int)  # 默认阈值0.5

    def _c(self, n):
        """计算路径长度的修正项(与IsolationTree中的实现一致)"""
        if n <= 1:
            return 0
        return 2 * (math.log(n - 1) + 0.5772156649) - (2 * (n - 1) / n)


def main():
    # 读取输入数据
    # 第一行：样本数量和特征数量
    N, M = map(int, input().split())

    # 接下来 N 行：样本特征值
    samples = []
    for _ in range(N):
        samples.append(list(map(float, input().split())))

    # 最后一行：孤立树数量和子样本大小
    T, psi = map(int, input().split())

    # 转换为 numpy 数组
    X = np.array(samples)

    # 训练孤立森林模型
    model = IsolationForest(n_trees=T, sample_size=psi)
    model.fit(X)

    # 预测异常分数和标签
    scores = model.anomaly_score(X)
    # 将分数归一化到 [0, 1] 范围，越小越正常，越大越异常
    scores = (scores - scores.min()) / (scores.max() - scores.min())
    labels = model.predict(X)

    # 输出结果
    for score, label in zip(scores, labels):
        print(f"{score:.4f} {label}")


if __name__ == "__main__":
    main()