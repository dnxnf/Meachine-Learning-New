# -*- coding: utf-8 -*-
"""修复可视化错误的Optuna示例"""

import optuna
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# 设置日志级别
optuna.logging.set_verbosity(optuna.logging.WARNING)

# 加载数据
print("正在加载数据...")
data = load_iris()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# 定义目标函数
def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 10, 200),
        'max_depth': trial.suggest_int('max_depth', 2, 20),
        'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy']),
        'min_samples_split': trial.suggest_float('min_samples_split', 0.01, 1.0),
        'min_samples_leaf': trial.suggest_float('min_samples_leaf', 0.01, 0.5),
        'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
    }

    model = RandomForestClassifier(**params, random_state=42, n_jobs=1)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy', n_jobs=4)
    return scores.mean()

# 运行优化
print("开始超参数优化...")
study = optuna.create_study(
    direction='maximize',
    study_name='random_forest_iris'
    # sampler=optuna.samplers.TPESampler(), # 默认就是TPE，可省略
    # pruner=optuna.pruners.MedianPruner()  # 如果需要提前终止，可加入剪枝器
)
study.optimize(objective, n_trials=100, show_progress_bar=True)

print("\n" + "=" * 50)
print("优化完成！")
print("=" * 50)

# 输出结果
print(f"\n总共完成了 {len(study.trials)} 次试验")
print(f"\n最佳准确率: {study.best_value:.4f}")
print("\n最佳超参数组合:")
for key, value in study.best_params.items():
    print(f"  {key}: {value}")

# 测试集评估
print("\n" + "-" * 30)
print("在测试集上评估最终模型...")
best_model = RandomForestClassifier(**study.best_params, random_state=42, n_jobs=-1)
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
print(f"测试集准确率: {test_accuracy:.4f}")

# 修复后的可视化部分
print("\n生成可视化图表...")

# 使用Matplotlib绘制优化历史
plt.figure(figsize=(12, 8))

# 子图1: 优化历史
plt.subplot(2, 2, 1)
values = [t.value for t in study.trials if t.value is not None]
numbers = [t.number for t in study.trials if t.value is not None]
plt.plot(numbers, values, 'b-o', alpha=0.7, markersize=4)
plt.xlabel('Trial Number')
plt.ylabel('Accuracy')
plt.title('Optimization History')
plt.grid(True, alpha=0.3)

# 子图2: 最佳值变化
plt.subplot(2, 2, 2)
best_values = [max(values[:i + 1]) for i in range(len(values))]
plt.plot(numbers, best_values, 'r-', linewidth=2)
plt.xlabel('Trial Number')
plt.ylabel('Best Accuracy')
plt.title('Best Value Progression')
plt.grid(True, alpha=0.3)

# 子图3: 参数分布（示例）
plt.subplot(2, 2, 3)
n_estimators_vals = [t.params.get('n_estimators', 0) for t in study.trials if t.value is not None]
plt.hist(n_estimators_vals, bins=20, alpha=0.7, edgecolor='black')
plt.xlabel('n_estimators')
plt.ylabel('Frequency')
plt.title('Parameter Distribution')
plt.grid(True, alpha=0.3)

# 子图4: 参数与性能关系
plt.subplot(2, 2, 4)
max_depth_vals = [t.params.get('max_depth', 0) for t in study.trials if t.value is not None]
plt.scatter(max_depth_vals, values, alpha=0.6, c=values, cmap='viridis')
plt.colorbar(label='Accuracy')
plt.xlabel('max_depth')
plt.ylabel('Accuracy')
plt.title('Parameter vs Performance')

plt.tight_layout()
plt.savefig('optuna_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("可视化图表已保存为 'optuna_analysis.png'")

# 文本形式的参数重要性分析
print("\n参数重要性分析:")
try:
    param_importance = optuna.importance.get_param_importances(study)
    for param, importance in param_importance.items():
        print(f"  {param}: {importance:.3f}")
except:
    print("  无法计算参数重要性")
