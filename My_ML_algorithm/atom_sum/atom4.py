#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：atom4.py
@Description ：模型预测结果可视化
@Author      ：Hello World
@Date        ：2025/6/6 下午4:15
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 定义模型（复用之前的预测函数）
def predict_segmented(has_extend_methyl: bool, carbon_count: int, hybridization: str) -> float:
    if hybridization == "sp2":
        return 1.25
    else:
        base_values = {
            3: (0.66, 0.70),
            2: (0.72, 0.74),
            1: (0.92, 0.91)
        }
        if carbon_count not in base_values:
            raise ValueError(f"不支持的碳原子数量: {carbon_count}")
        return base_values[carbon_count][1] if has_extend_methyl else base_values[carbon_count][0]

def predict_linear(has_extend_methyl: bool, carbon_count: int, hybridization: str) -> float:
    extend_code = 1 if has_extend_methyl else 0
    hybrid_code = 1 if hybridization == "sp2" else 0
    coefficients = {
        'intercept': 1.194,
        'carbon': -0.182,
        'extend': 0.011,
        'hybrid': 0.333
    }
    prediction = (
        coefficients['intercept'] +
        coefficients['carbon'] * carbon_count +
        coefficients['extend'] * extend_code +
        coefficients['hybrid'] * hybrid_code
    )
    return max(0.6, min(1.3, prediction))

# 打印模型关系式
print("分段模型关系式:")
print("1. 对于sp2杂化: 固定预测值 = 1.25")
print("2. 对于sp3杂化:")
print("   - 碳原子数3: 无甲基延伸=0.66, 有甲基延伸=0.70")
print("   - 碳原子数2: 无甲基延伸=0.72, 有甲基延伸=0.74")
print("   - 碳原子数1: 无甲基延伸=0.92, 有甲基延伸=0.91")

print("\n线性模型关系式:")
print("预测值 = 1.194 + (-0.182 × 碳原子数) + (0.011 × 甲基延伸) + (0.333 × 杂化类型)")
print("其中: 甲基延伸(有=1,无=0), 杂化类型(sp2=1,sp3=0)")
print("最终预测值限制在[0.6, 1.3]范围内")

# 生成所有可能的输入组合
carbon_counts = [3, 2, 1]
extend_options = [False, True]
hybrid_options = ["sp3", "sp2"]

data = []
for cc in carbon_counts:
    for extend in extend_options:
        for hybrid in hybrid_options:
            seg_pred = predict_segmented(extend, cc, hybrid)
            lin_pred = predict_linear(extend, cc, hybrid)
            data.append({
                "Carbon Count": cc,
                "Extend Methyl": "有" if extend else "无",
                "Hybridization": hybrid,
                "Segmented Model": seg_pred,
                "Linear Model": lin_pred
            })

df = pd.DataFrame(data)

# 打印前几行数据
print("\n生成的部分预测数据:")
print(df.head())

# 将数据从宽格式转换为长格式
df_melted = df.melt(id_vars=["Carbon Count", "Extend Methyl", "Hybridization"],
                    value_vars=["Segmented Model", "Linear Model"],
                    var_name="Model", value_name="Prediction")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建画布
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# 绘制分面图
g = sns.FacetGrid(df_melted, col="Hybridization",
                  hue="Extend Methyl",
                  palette={"无": "blue", "有": "orange"},
                  height=6, aspect=1.2, sharey=False)

# 绘制模型预测线，区分不同模型
g.map(sns.lineplot, "Carbon Count", "Prediction",
      markers=True, dashes=False, lw=3, alpha=0.8,
      style_order=["Segmented Model", "Linear Model"])

# 添加图例
g.add_legend()

# 添加实际数据点（测试用例）
test_cases = [
    (False, 3, "sp3", 0.66),
    (True, 3, "sp3", 0.70),
    (False, 2, "sp3", 0.72),
    (True, 2, "sp3", 0.74),
    (False, 1, "sp3", 0.92),
    (True, 1, "sp3", 0.91),
    (False, 1, "sp2", 1.25),
    (True, 1, "sp2", 1.25)
]

test_df = pd.DataFrame(test_cases, columns=["Extend Methyl", "Carbon Count",
                                          "Hybridization", "Actual Value"])
test_df["Extend Methyl"] = test_df["Extend Methyl"].map({False: "无", True: "有"})

# 在每个子图上添加散点
for (hybrid, hue), subset in test_df.groupby(["Hybridization", "Extend Methyl"]):
    ax = g.axes[0, 0] if hybrid == "sp3" else g.axes[0, 1]
    sns.scatterplot(data=subset, x="Carbon Count", y="Actual Value",
                    hue="Extend Methyl", style="Extend Methyl",
                    markers=["o", "s"], s=100,
                    palette={"无": "blue", "有": "orange"},
                    ax=ax, legend=False)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 图表装饰
g.set_titles(col_template="{col_name}杂化")
g.set_xlabels("碳原子数量")
g.set_ylabels("预测值")
g.set(ylim=(0.5, 1.35))

plt.suptitle("不同条件下两模型预测结果对比", y=0.94, fontsize=16)
plt.tight_layout()
plt.savefig("model_comparison.png", dpi=300, bbox_inches="tight")
plt.show()