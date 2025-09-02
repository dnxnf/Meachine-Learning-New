#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：LLaVALearn.py
@Description ：
@Author      ：Hello World
@Date        ：2025/8/31 下午3:31 
'''
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message=".*torchvision.datapoints.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*torchvision.transforms.v2.*")
from PIL import Image
import matplotlib.pyplot as plt  # 更快的显示方式

dataPath = "..\CV_python\wen.jpg"


def showImage():
    image = Image.open(dataPath)
    image.show()


def runLLaVA():
    from transformers import LlavaNextForConditionalGeneration, LlavaNextProcessor
    import torch

    # 1. 指定模型ID。LLaVA 团队在 HF 上提供了多个版本。
    # 例如，我们使用较小的 LLaVA-1.5 7B 模型
    model_id = "llava-hf/llava-1.5-7b-hf"

    # 2. 加载处理器（负责处理图像和文本）和模型
    #    首次运行时会自动从 Hugging Face Hub 下载模型权重和配置文件，无需手动下载。
    processor = LlavaNextProcessor.from_pretrained(model_id)
    model = LlavaNextForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.float16,  # 使用半精度减少显存占用
        device_map="auto",  # 自动将模型层分配到可用的GPU和CPU上
    )

    # 3. 准备输入
    # 3.1 准备一张图片

    image = Image.open(dataPath)  # 请替换成你的图片路径
    # 3.2 构造一个符合 LLaVA 要求的对话提示词
    prompt = "USER: <Image>\nWhat are the key elements in this Image?\nASSISTANT:"
    inputs = processor(prompt, image, return_tensors="pt").to(model.device)

    # 4. 生成回答
    # 将输入传递给模型并生成输出
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=100)
    # 解码生成的 token IDs 为文本
    answer = processor.decode(output[0], skip_special_tokens=True)

    print(answer)
if __name__ == '__main__':
    showImage()
    # runLLaVA()