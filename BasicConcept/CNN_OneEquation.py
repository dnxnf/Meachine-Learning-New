#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：CNN_OneEquation.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/29 上午11:44
一元一次方程的线性回归, 使用神经网络拟合a,b, 使用均方误差损失函数, 使用随机梯度下降优化器, 使用PyTorch

'''
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# 1. 生成训练数据
# 定义一元一次方程的系数
a_true = float(input("请输入一元一次方程的系数a（例如：2）: "))
b_true = float(input("请输入一元一次方程的截距b（例如：1）: "))

# 生成输入数据x（范围在-10到10之间）
x = np.linspace(-10, 10, 1000).reshape(-1, 1)  # 1000个样本，形状为(1000, 1)
y = a_true * x + b_true  # 真实的y值

# 添加噪声（模拟真实数据中的噪声）
noise = np.random.normal(0, 1, size=x.shape)  # 均值为0，标准差为1的高斯噪声
# noise = 0
y_noisy = y + noise  # 带噪声的y值

# 转换为PyTorch张量
x_tensor = torch.tensor(x, dtype=torch.float32)
y_tensor = torch.tensor(y_noisy, dtype=torch.float32)


# 2. 定义神经网络模型
class LinearRegressionNN(nn.Module):
    def __init__(self, input_size, output_size):
        """
        初始化神经网络结构
        参数:
            input_size: 输入层特征数（这里是1，因为x是单变量）
            output_size: 输出层维度（这里是1，因为y是单变量）
        """
        super(LinearRegressionNN, self).__init__()
        self.linear = nn.Linear(input_size, output_size)  # 单层线性网络（相当于y = wx + b）

    def forward(self, x):
        """
        定义前向传播过程
        参数:
            x: 输入数据
        返回:
            模型的输出
        """
        out = self.linear(x)  # 线性层直接输出
        return out


# 3. 初始化模型、损失函数和优化器
input_size = 1  # 输入特征数（x是单变量）
output_size = 1  # 输出维度（y是单变量）

model = LinearRegressionNN(input_size, output_size)
criterion = nn.MSELoss()  # 均方误差损失函数（适用于回归问题）
optimizer = optim.SGD(model.parameters(), lr=0.01)  # 随机梯度下降优化器

# 4. 训练模型
num_epochs = 1000  # 训练轮数

loss_history = []  # 记录损失变化

for epoch in range(num_epochs):
    # 前向传播
    outputs = model(x_tensor)
    loss = criterion(outputs, y_tensor)

    # 反向传播和优化
    optimizer.zero_grad()  # 清空梯度
    loss.backward()  # 反向传播计算梯度
    optimizer.step()  # 更新参数

    # 记录损失
    loss_history.append(loss.item())

    # 打印每100轮的损失
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# 5. 可视化结果
# 提取训练后的参数
w_trained = model.linear.weight.item()  # 训练后的权重（相当于a）
b_trained = model.linear.bias.item()  # 训练后的偏置（相当于b）

print(f'True parameters: a={a_true}, b={b_true}')
print(f'Trained parameters: a={w_trained:.4f}, b={b_trained:.4f}')

# 绘制真实曲线和预测曲线
plt.figure(figsize=(10, 6))
plt.scatter(x, y_noisy, label='Noisy Data', alpha=0.5)  # 带噪声的数据点
plt.plot(x, y, 'r-', label=f'True Line: y = {a_true}x + {b_true}', linewidth=2)  # 真实曲线
plt.plot(x, outputs.detach().numpy(), 'g--', label=f'Predicted Line: y = {w_trained:.2f}x + {b_trained:.2f}',
         linewidth=2)  # 预测曲线
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Regression with Neural Network')
plt.legend()
x_min, x_max = 0, 10  # 只显示x从0到10的部分
y_min, y_max = 0, a_true * x_max + b_true + 2  # y的范围根据x的最大值计算
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.show()

# 绘制损失变化曲线
plt.figure(figsize=(10, 6))
plt.plot(loss_history, label='Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Curve')
plt.legend()
plt.show()
