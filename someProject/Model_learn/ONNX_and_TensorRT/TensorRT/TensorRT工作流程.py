#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：TensorRT工作流程.py
@Description ：
@Author      ：Hello World
@Date        ：2025/8/27 下午6:03 
'''
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np

# 1. 创建 TensorRT 构建器
logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)

# 2. 创建网络定义
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))

# 3. 创建 ONNX 解析器
parser = trt.OnnxParser(network, logger)

# 4. 解析 ONNX 模型
with open("../ONNX/model.onnx", "rb") as model:
    if not parser.parse(model.read()):
        for error in range(parser.num_errors):
            print(parser.get_error(error))

# 5. 创建构建配置
config = builder.create_builder_config()
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)  # 1GB

# 6. 构建引擎
serialized_engine = builder.build_serialized_network(network, config)

# 7. 保存引擎
with open("model.engine", "wb") as f:
    f.write(serialized_engine)

# 加载 TensorRT 引擎
runtime = trt.Runtime(logger)
with open("model.engine", "rb") as f:
    engine = runtime.deserialize_cuda_engine(f.read())

# 创建执行上下文
context = engine.create_execution_context()

# 分配 GPU 内存
h_input = np.random.rand(1, 5).astype(np.float32)
d_input = cuda.mem_alloc(h_input.nbytes)
h_output = np.empty((1, 2), dtype=np.float32)
d_output = cuda.mem_alloc(h_output.nbytes)

# 创建流
stream = cuda.Stream()

# 执行推理
cuda.memcpy_htod_async(d_input, h_input, stream)
context.execute_async_v2(bindings=[int(d_input), int(d_output)], stream_handle=stream.handle)
cuda.memcpy_dtoh_async(h_output, d_output, stream)
stream.synchronize()

print("TensorRT 预测结果:", h_output)