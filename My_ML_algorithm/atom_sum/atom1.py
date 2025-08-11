#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：atom1.py
@Description ：方程1 讨论与中心碳所连原子的电负性对亲电性的影响
@Author      ：Hello World
@Date        ：2025/6/6 下午3:10 
'''
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 构建包含碳氢独立求和的数据集
data = {
    '连接原子类型': ['C-C-C', 'C-C-H', 'C-H-H'],
    '杂化状态': ['sp3', 'sp3', 'sp3'],
    '亲电性': [0.66, 0.72, 0.89]
}
df = pd.DataFrame(data)

# 原子电负性映射
atom_mapping = {'C': 2.55, 'H': 2.2}

# 拆解原子类型并计算碳氢贡献
df['原子列表'] = df['连接原子类型'].str.split('-')
df['C_count'] = df['原子列表'].apply(lambda x: x.count('C'))
df['H_count'] = df['原子列表'].apply(lambda x: x.count('H'))
df['C_sum'] = df['C_count'] * atom_mapping['C']
df['H_sum'] = df['H_count'] * atom_mapping['H']

# 清理中间变量
df.drop(columns=['原子列表', 'C_count', 'H_count'], inplace=True)

# 构建特征矩阵（仅使用碳氢电负性贡献）
X = df[['C_sum', 'H_sum']]
y = df['亲电性']

# 训练线性回归模型
model = LinearRegression()
model.fit(X, y)

# 输出结果
print(f"亲电性方程: 亲电性 = {model.coef_[0]:.4f}×C电负性总和 + {model.coef_[1]:.4f}×H电负性总和 + {model.intercept_:.4f}")
print(f"R^2分数: {model.score(X, y):.3f}")

# 可视化三维关系（可选）
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['C_sum'], df['H_sum'], df['亲电性'], c='r', marker='o')

# 生成预测平面
x_surf, y_surf = np.meshgrid(
    np.linspace(df['C_sum'].min(), df['C_sum'].max(), 10),
    np.linspace(df['H_sum'].min(), df['H_sum'].max(), 10)
)
z_pred = model.predict(np.c_[x_surf.ravel(), y_surf.ravel()]).reshape(x_surf.shape)

ax.plot_surface(x_surf, y_surf, z_pred, alpha=0.3)
ax.set_xlabel('C电负性总和')
ax.set_ylabel('H电负性总和')
ax.set_zlabel('亲电性')
plt.show()