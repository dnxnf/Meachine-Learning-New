#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：PCA_SVM.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/5 下午5:32 
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.svm import SVC

# 生成数据
np.random.seed(42)
X = np.r_[np.random.randn(20, 2) + [2, 2], np.random.randn(20, 2) + [-2, -2]]
y = np.array([1] * 20 + [0] * 20)

# PCA投影
pca = PCA(n_components=1)
X_pca = pca.fit_transform(X)

# SVM投影（线性核）
svm = SVC(kernel='linear')
svm.fit(X, y)
w = svm.coef_[0]
svm_proj = X.dot(w)

# 绘图
plt.figure(figsize=(12, 5))
plt.subplot(121)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr')
plt.arrow(0, 0, pca.components_[0, 0], pca.components_[0, 1], width=0.1, color='black')
plt.title("PCA投影方向（最大方差方向）")

plt.subplot(122)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr')
plt.arrow(0, 0, w[0], w[1], width=0.1, color='black')
plt.title("SVM投影方向（最大间隔方向）")
plt.show()
