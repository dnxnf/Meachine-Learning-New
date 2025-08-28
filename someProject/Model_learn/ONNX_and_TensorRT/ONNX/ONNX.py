#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：ONNX.py
@Description ：
@Author      ：Hello World
@Date        ：2025/8/27 下午5:46 
'''
import torch
import torch.onnx
from sklearn.ensemble import RandomForestClassifier
import onnx
import onnxruntime as ort
import numpy as np

# 1. 训练一个简单模型
model = RandomForestClassifier(n_estimators=10, random_state=42)
X = np.random.rand(100, 5)
y = np.random.randint(0, 2, 100)
model.fit(X, y)

# 2. 使用 skl2onnx 转换 sklearn 模型
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# 定义输入类型
initial_type = [('float_input', FloatTensorType([None, 5]))]

# 转换为 ONNX 格式
onnx_model = convert_sklearn(model, initial_types=initial_type)

# 3. 保存 ONNX 模型
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# 4. 使用 ONNX Runtime 进行推理
ort_session = ort.InferenceSession("model.onnx")

# 准备输入数据
input_name = ort_session.get_inputs()[0].name
input_data = np.random.rand(1, 5).astype(np.float32)

# 进行预测
outputs = ort_session.run(None, {input_name: input_data})
print("ONNX 预测结果:", outputs[0])