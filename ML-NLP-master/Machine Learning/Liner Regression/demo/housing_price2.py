from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 设置随机种子
np.random.seed(36)

# 1. 数据读取
try:
    housing = pd.read_csv("kc_train.csv")
    test_data = pd.read_csv("kc_test.csv")
except Exception as e:
    print(f"文件读取错误: {e}")
    exit()

# 2. 检查数据
print("训练数据前5行:")
print(housing.head())
print("\n测试数据前5行:")
print(test_data.head())

# 3. 分离特征和目标（假设最后一列是目标）
X = housing.iloc[:, :-1]  # 所有特征列
y = housing.iloc[:, 1]  # 目标列（假设是最后一列）

# 4. 特征缩放（仅对特征）
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 5. 模型训练
model = LinearRegression()
model.fit(X_scaled, y)

# 6. 预测和评估
preds = model.predict(X_scaled)
mse = mean_squared_error(y, preds)
print(f"\n模型评估:")
print(f"MSE: {mse:.2f}")
print(f"前5个预测值: {preds[:5]}")
print(f"前5个实际值: {y.values[:5]}")

# 7. 绘图
plt.figure(figsize=(12, 6))
num = min(100, len(y))  # 比较前100个点

# 确保使用相同的数据类型
plt.plot(y.values[:num], "b-", label="实际值", alpha=0.7)
plt.plot(preds[:num], "r--", label="预测值", alpha=0.7)

plt.title("房价实际值与预测值对比", fontsize=14)
plt.xlabel("样本索引", fontsize=12)
plt.ylabel("房价", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# 8. 测试集预测
try:
    test_scaled = scaler.transform(test_data)  # 使用相同的缩放器
    test_pred = model.predict(test_scaled)
    pd.DataFrame(test_pred).to_csv("result.csv", index=False, header=False)
    print("\n测试集预测结果已保存到result.csv")
except Exception as e:
    print(f"\n测试集预测错误: {e}")
