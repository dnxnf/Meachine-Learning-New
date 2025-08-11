import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 原始数据
mapping = {
    (False, 3, "sp3"): 0.66,
    (True, 3, "sp3"): 0.70,
    (False, 2, "sp3"): 0.72,
    (True, 2, "sp3"): 0.74,
    (False, 1, "sp3"): 0.92,
    (True, 1, "sp3"): 0.91,
    (False, 1, "sp2"): 1.25,
    (True, 1, "sp2"): 1.25
}

# 准备数据
data = []
for (bool_val, num, sp_type), target in mapping.items():
    data.append([bool_val, num, sp_type, target])
df = pd.DataFrame(data, columns=['bool', 'num', 'sp_type', 'target'])

# 特征预处理管道
preprocessor = ColumnTransformer(
    transformers=[
        ('bool', 'passthrough', ['bool']),
        ('num', StandardScaler(), ['num']),
        ('cat', OneHotEncoder(), ['sp_type'])
    ])

# 构建岭回归模型
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', Ridge(alpha=1.0, random_state=42))
])

# 训练模型
X = df[['bool', 'num', 'sp_type']]
y = df['target']
model.fit(X, y)

# 提取模型参数
intercept = model.named_steps['regressor'].intercept_
coef = model.named_steps['regressor'].coef_
feature_names = model.named_steps['preprocessor'].get_feature_names_out()

# 获取标准化参数（num列的均值和标准差）
num_scaler = model.named_steps['preprocessor'].named_transformers_['num']
num_mean = num_scaler.mean_[0]
num_std = num_scaler.scale_[0]

# 打印岭回归方程
print("=" * 50)
print("岭回归方程 f(x):")
print(f"f(bool, num, sp_type) = {intercept:.4f}")

for name, c in zip(feature_names, coef):
    # 方法1：直接打印所有特征（最保险）
    print(f" + {c:.4f} * [{name}]")

    # 或方法2：使用包含判断（更友好但需要适配实际特征名）
    # if 'bool' in name.lower():
    #     print(f" + {c:.4f} * bool")
    # elif 'num' in name.lower():
    #     print(f" + {c:.4f} * (num标准化值)")
    # elif 'sp2' in name.lower():
    #     print(f" + {c:.4f} * sp2")
    # elif 'sp3' in name.lower():
    #     print(f" + {c:.4f} * sp3")

# 打印预处理规则
print("\n预处理规则:")
print(f"- bool: False → 0, True → 1")
print(f"- num: 标准化 (x - {num_mean:.1f}) / {num_std:.4f}")
print(f"- sp_type: 独热编码（sp2 → [1, 0], sp3 → [0, 1]）")

# 打印实际参数值
print("\n实际参数值:")
print(f"截距 (Intercept) = {intercept:.4f}")
for name, c in zip(feature_names, coef):
    print(f"{name} 的系数 = {c:.4f}")