#!/usr/bin/env python
# coding=utf-8
'''
基于ID3算法，使用信息增益来选择最佳特征
'''
import os
import time
import numpy as np
# 导入处于不同目录下的Mnist.load_data
import sys, os.path as osp

sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))
current_working_dir = os.getcwd()
print(f"当前工作目录: {current_working_dir}")
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"脚本所在目录: {script_dir}")
from ML_Sklearn_code.datasets.MNIST.raw.load_data import *


class DecisionTree:
    def __init__(self, x_train, y_train, x_test, y_test):
        '''
        Args:
            x_train [Array]: 训练集数据
            y_train [Array]: 训练集标签
            x_test [Array]: 测试集数据
            y_test [Array]: 测试集标签
        '''
        self.x_train, self.y_train = x_train, y_train
        self.x_test, self.y_test = x_test, y_test
        # 将输入数据转为矩阵形式，方便运算
        self.x_train_mat, self.x_test_mat = np.asmatrix(
            self.x_train), np.asmatrix(self.x_test)
        self.y_train_mat, self.y_test_mat = np.asmatrix(
            self.y_train).T, np.asmatrix(self.y_test).T

        # 设置epsilon阈值
        self.epsilon_threshhold = 0.1
        self.tree = {}  # 保存生成的树为字典

    def majorClass(self, labelArr):
        '''
        找到当前标签集中占数目最大的标签
        :param labelArr: 标签集
        :return: 最大的标签
        '''
        classDict = {}
        for i in range(len(labelArr)):
            if labelArr[i] in classDict.keys():
                classDict[labelArr[i]] += 1
            else:
                classDict[labelArr[i]] = 1
        classSort = sorted(classDict.items(), key=lambda x: x[1], reverse=True)
        return classSort[0][0]

    def calcShannonEnt(self, y_train):
        """
        计算香农熵
        :param y_train: 训练数据标签
        :return: 香农熵
        """
        num_entries = len(y_train)
        label_counts = {}
        for label in y_train:
            if label not in label_counts.keys():
                label_counts[label] = 0
            label_counts[label] += 1

        shannon_ent = 0.0
        for key in label_counts:
            prob = float(label_counts[key]) / num_entries
            shannon_ent -= prob * np.log2(prob)

        return shannon_ent

    def calcBestFeature(self, x_train, y_train):
        """
        计算最佳特征分割
        :param x_train: 训练数据特征
        :param y_train: 训练数据标签
        :return: 最佳特征索引和对应的信息增益
        """
        num_features = x_train.shape[1]
        best_feature = -1
        best_info_gain = -1

        # 计算原始数据集的熵
        base_entropy = self.calcShannonEnt(y_train)

        for i in range(num_features):
            # 获取当前特征的所有可能值
            feat_values = x_train[:, i]
            unique_values = set(feat_values)

            # 计算当前特征的信息增益
            new_entropy = 0.0
            for value in unique_values:
                sub_y_train = y_train[feat_values == value]
                prob = len(sub_y_train) / len(y_train)
                new_entropy += prob * self.calcShannonEnt(sub_y_train)

            info_gain = base_entropy - new_entropy

            # 更新最佳特征
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_feature = i

        return best_feature, best_info_gain

    @staticmethod
    def getSubDataArr(dataSet, labels, feature, value):
        """
        根据特征值分割数据集
        :param dataSet: 特征矩阵
        :param labels: 标签数组
        :param feature: 特征索引
        :param value: 特征值
        :return: 子数据集和子标签
        """
        retData = []
        retLabels = []
        for i in range(len(dataSet)):
            if dataSet[i, feature] == value:
                retData.append(dataSet[i, :])
                retLabels.append(labels[i])
        return np.array(retData), np.array(retLabels)

    def createTree(self, dataSet, labels):
        """
        递归创建决策树
        :param dataSet: 当前数据集特征
        :param labels: 当前数据集标签
        :return: 构建好的决策树（字典）
        """
        classList = labels.flatten().tolist()

        # 统一返回字典结构
        if len(classList) == 0 or len(set(classList)) == 1:
            return {None: classList[0]} if classList else {None: self.majorClass(self.y_train)}

        if len(dataSet) == 0 or len(dataSet[0]) == 0:  # 处理空数据集
            return {None: self.majorClass(np.array(classList))}

        bestFeat, infoGain = self.calcBestFeature(dataSet, labels)

        if infoGain < self.epsilon_threshhold:
            return {None: self.majorClass(np.array(classList))}

        tree = {bestFeat: {}}
        featValues = dataSet[:, bestFeat]
        uniqueValues = np.unique(featValues)

        for value in uniqueValues:
            subDataSet, subLabels = self.getSubDataArr(dataSet, labels, bestFeat, value)
            subtree = self.createTree(subDataSet, subLabels)
            tree[bestFeat][value] = subtree

        return tree

    def train(self):
        print('start a node', len(self.x_train[0]), len(self.y_train))
        classDict = {i for i in self.y_train}

        if len(classDict) == 1:
            return {None: self.y_train[0]}

        if len(self.x_train[0]) == 0:
            return {None: self.majorClass(self.y_train)}

        Ag, EpsilonGet = self.calcBestFeature(self.x_train, self.y_train)

        if EpsilonGet < self.epsilon_threshhold:
            return {None: self.majorClass(self.y_train)}

        # 分割数据集
        sub_x_0, sub_y_0 = self.getSubDataArr(self.x_train, self.y_train, Ag, 0)
        sub_x_1, sub_y_1 = self.getSubDataArr(self.x_train, self.y_train, Ag, 1)

        treeDict = {Ag: {}}
        treeDict[Ag][0] = self.createTree(sub_x_0, sub_y_0)
        treeDict[Ag][1] = self.createTree(sub_x_1, sub_y_1)

        return treeDict

if __name__ == "__main__":
    # 开始时间
    start = time.time()
    # print('start time:', start)
    (x_train, y_train), (x_test, y_test) = load_local_mnist(one_hot=False)
    # note 下两行是大数据集
    # model = DecisionTree(x_train, y_train, x_test, y_test)
    # print(model.train())

    # 创建一个小型测试数据集
    # 特征1: 颜色 (0-红, 1-蓝)
    # 特征2: 形状 (0-圆, 1-方)
    # 标签: 是否为水果 (0-否, 1-是)
    x_train = np.array([
        [0, 0],  # 红且圆 → 是水果
        [0, 1],  # 红且方 → 不是水果
        [1, 0],  # 蓝且圆 → 是水果
        [1, 1]  # 蓝且方 → 不是水果
    ])

    y_train = np.array([1, 0, 1, 0])
    model = DecisionTree(x_train, y_train, None, None)
    tree = model.train()
    print("生成的决策树:", tree)