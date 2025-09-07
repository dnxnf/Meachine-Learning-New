#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：LogisticRegression.py
@Description ：手写逻辑回归算法,逻辑回归，实际上是分类
@Author      ：Hello World
@Date        ：2025/9/6 下午9:37 
'''
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class LogisticRegression:
    def __init__(self, learning_rate=0.01, num_iterations=1000):
        """
        初始化逻辑回归模型

        参数:
        learning_rate: 学习率，控制梯度下降的步长大小
        num_iterations: 迭代次数，决定训练轮数
        """
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None  # 权重参数，每个特征对应一个权重
        self.bias = None  # 偏置参数，调整决策边界的位置

    def sigmoid(self, z):
        """
        Sigmoid激活函数，将线性输出映射到(0,1)区间

        参数:
        z: 线性模型的输出值

        返回:
        经过sigmoid变换后的概率值
        """
        z = np.clip(z, -500, 500)  # 避免数值溢出
        return 1 / (1 + np.exp(-z))

    def init_Parameters(self, n_features):
        """
        初始化模型参数

        参数:
        n_features: 特征数量，决定权重向量的长度
        """
        # 权重初始化为0向量，长度等于特征数
        # self.weights = np.zeros(n_features)
        self.weights = np.random.randn(n_features) * 0.1  # 随机初始化权重
        # 偏置初始化为0
        self.bias = 0

    def compute_loss(self, y, y_pred):
        """
        计算二分类交叉熵损失函数

        参数:
        y: 真实标签值 (0或1)
        y_pred: 预测概率值 (0-1之间)

        返回:
        平均交叉熵损失值
        """
        epsilon = 1e-15
        # 限制预测概率范围，避免log(0)的情况
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        # 交叉熵损失公式: -[y*log(p) + (1-y)*log(1-p)]
        loss = -np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))
        return loss

    def fit(self, X, y):
        """
        训练逻辑回归模型

        参数:
        X: 特征矩阵，形状为 (n_samples, n_features)
        y: 目标向量，形状为 (n_samples,)

        返回:
        self: 训练好的模型实例
        """
        n_samples, n_features = X.shape
        # 1. 初始化参数
        self.init_Parameters(n_features)

        # 2. 梯度下降迭代训练
        for i in range(self.num_iterations):
            # 2.1 前向传播
            # 计算线性组合: z = w·x + b
            z = np.dot(X, self.weights) + self.bias
            # 左列乘右行得到左行右列，即矩阵乘法
            # 应用sigmoid函数得到预测概率
            y_pred = self.sigmoid(z)

            # 2.2 计算当前损失
            loss = self.compute_loss(y, y_pred)

            # 2.3 反向传播（计算梯度）
            # 梯度计算公式:
            # ∂L/∂w = (1/n) * X^T · (y_pred - y)
            # ∂L/∂b = (1/n) * Σ (y_pred - y)
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            # 2.4 梯度下降更新参数
            # w = w - α * ∂L/∂w
            # b = b - α * ∂L/∂b
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            # 2.5 打印训练进度
            if i % 100 == 0:
                print(f"Iteration {i}: loss = {loss:.6f}")

        return self # 返回实例对象本身

    def predict_prob(self, X):
        """
        预测样本属于正类的概率

        参数:
        X: 特征矩阵

        返回:
        预测概率向量，形状为 (n_samples,)
        """
        # 计算线性输出: z = w·x + b
        linear_model = np.dot(X, self.weights) + self.bias
        # 应用sigmoid得到概率
        return self.sigmoid(linear_model)

    def predict(self, X, threshold=0.5):
        """
        预测样本类别

        参数:
        X: 特征矩阵
        threshold: 分类阈值，默认0.5

        返回:
        预测类别向量 (0或1)，形状为 (n_samples,)
        """
        # 获取预测概率
        y_pred_prob = self.predict_prob(X)
        # 根据阈值进行分类决策
        return (y_pred_prob >= threshold).astype(int)

    def score(self, X, y):
        """
        计算模型准确率

        参数:
        X: 特征矩阵
        y: 真实标签

        返回:
        准确率值 (0-1之间)
        """
        y_pred = self.predict(X)
        accuracy = np.mean(y_pred == y)
        return accuracy

    def get_params(self):
        """
        获取模型参数

        返回:
        包含权重和偏置的字典
        """
        return {
            'weights': self.weights,
            'bias': self.bias,
        }


# 模型测试代码
def test_logistic_regression():
    """
    测试逻辑回归模型的完整流程
    """
    print("=" * 50)
    print("开始测试逻辑回归模型")
    print("=" * 50)

    # 1. 生成模拟数据
    print("1. 生成模拟数据集...")
    X, y = make_classification(
        n_samples=1000,  # 总样本数
        n_features=4,  # 特征数量
        n_informative=2,  # 有信息的特征数
        n_redundant=0,  # 冗余特征数
        n_clusters_per_class=1,
        random_state=42  # 随机种子
    )
    print(f"数据集形状: X={X.shape}, y={y.shape}")

    # 2. 数据预处理
    print("\n2. 数据预处理（标准化）...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("数据标准化完成")

    # 3. 划分训练集和测试集
    print("\n3. 划分训练集和测试集...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    print(f"训练集: {X_train.shape}, 测试集: {X_test.shape}")

    # 4. 创建和训练模型
    print("\n4. 创建并训练逻辑回归模型...")
    model = LogisticRegression(
        learning_rate=0.1,  # 学习率
        num_iterations=1000  # 迭代次数
    )

    print("开始训练...")
    model.fit(X_train, y_train)
    print("训练完成!")

    # 5. 评估模型性能
    print("\n5. 评估模型性能...")
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)

    print(f"训练集准确率: {train_accuracy:.4f}")
    print(f"测试集准确率: {test_accuracy:.4f}")

    # 6. 查看模型参数
    print("\n6. 查看模型参数...")
    params = model.get_params()
    print(f"权重参数: {params['weights']}")
    print(f"偏置参数: {params['bias']:.6f}")

    # 7. 进行预测示例
    print("\n7. 预测示例...")
    # 取前5个测试样本进行预测
    sample_indices = range(5)
    X_sample = X_test[sample_indices]
    y_sample_true = y_test[sample_indices]
    y_sample_pred = model.predict(X_sample)
    y_sample_prob = model.predict_prob(X_sample)

    print("前5个测试样本的预测结果:")
    for i in range(len(X_sample)):
        print(f"样本{i + 1}: 真实值={y_sample_true[i]}, "
              f"预测值={y_sample_pred[i]}, "
              f"概率={y_sample_prob[i]:.4f}")

    print("\n" + "=" * 50)
    print("模型测试完成!")
    print("=" * 50)


# 运行测试
if __name__ == "__main__":
    test_logistic_regression()
    # print("=" * 50)