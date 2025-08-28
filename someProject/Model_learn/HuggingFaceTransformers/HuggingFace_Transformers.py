#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：HuggingFace_Transformers.py
@Description ：
@Author      ：Hello World
@Date        ：2025/8/27 下午6:13 
'''
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch


def show_models():
    # 1. 使用pipeline（最简单的方式）
    print("=== 使用Pipeline ===")
    classifier = pipeline("sentiment-analysis")
    result = classifier("I love this movie! It's amazing!")
    print("情感分析结果:", result)

    # 2. 文本生成
    generator = pipeline("text-generation", model="gpt2")
    result = generator("The future of AI is", max_length=30, num_return_sequences=1)
    print("文本生成:", result[0]['generated_text'])

    # 3. 更细粒度的控制
    print("\n=== 细粒度控制 ===")
    # 加载tokenizer和模型
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # 处理文本
    text = "This is a great tutorial about HuggingFace!"
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # 推理
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        print("预测概率:", predictions)

flag = input("你是否要使用HuggingFace Transformers，他会下载一些模型，需要一些时间？(y/n)")
if flag.lower() == "y":
    show_models()
else:
    print("不使用HuggingFace Transformers，那就谢谢啦！")
