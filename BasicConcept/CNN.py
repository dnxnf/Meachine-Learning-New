#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：CNN.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/29 上午11:40 
'''
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# 1. 准备数据
# 生成示例数据：100个样本，每个样本有3个特征
X = np.random.randn(100, 3)  # 100个样本，3个特征
# print(X)
y = (X[:, 0] + 2 * X[:, 1] - 1.5 * X[:, 2] > 0).astype(int)  # 简单的线性分类标签

# 转换为PyTorch张量
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)  # 调整形状为(100, 1)

# 创建数据集和数据加载器
dataset = TensorDataset(X_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=10, shuffle=True)


# 2. 定义神经网络模型
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        """
        初始化神经网络结构
        参数:
            input_size: 输入层特征数
            hidden_size: 隐藏层神经元数量
            output_size: 输出层维度
        """
        super(SimpleNN, self).__init__()
        # 定义网络层
        self.fc1 = nn.Linear(input_size, hidden_size)  # 输入层到隐藏层
        self.relu = nn.ReLU()  # 激活函数
        self.fc2 = nn.Linear(hidden_size, output_size)  # 隐藏层到输出层
        self.sigmoid = nn.Sigmoid()  # 输出层激活函数（用于二分类）

    def forward(self, x):
        """
        定义前向传播过程
        参数:
            x: 输入数据
        返回:
            模型的输出
        """
        out = self.fc1(x)  # 输入层 -> 隐藏层
        out = self.relu(out)  # 应用ReLU激活函数
        out = self.fc2(out)  # 隐藏层 -> 输出层
        out = self.sigmoid(out)  # 应用Sigmoid激活函数（将输出压缩到[0,1]）
        return out


# 3. 初始化模型、损失函数和优化器
input_size = 3  # 输入特征数（与数据一致）
hidden_size = 5  # 隐藏层神经元数量（可调整）
output_size = 1  # 输出维度（二分类问题）

model = SimpleNN(input_size, hidden_size, output_size)
criterion = nn.BCELoss()  # 二分类交叉熵损失函数
optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam优化器

# 4. 训练模型
num_epochs = 50  # 训练轮数

for epoch in range(num_epochs):
    for batch_X, batch_y in dataloader:  # 批量加载数据
        # 前向传播
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        # 反向传播和优化
        optimizer.zero_grad()  # 清空梯度
        loss.backward()  # 反向传播计算梯度
        optimizer.step()  # 更新参数

    # 打印每轮的损失
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# 5. 测试模型
with torch.no_grad():  # 禁用梯度计算（测试阶段）
    test_output = model(X_tensor)
    predicted = (test_output > 0.5).float()  # 以0.5为阈值进行分类
    accuracy = (predicted == y_tensor).float().mean()
    print(f'Test Accuracy: {accuracy.item() * 100:.2f}%')