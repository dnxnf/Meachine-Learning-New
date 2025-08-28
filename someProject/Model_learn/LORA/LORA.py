#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：LORA.py
@Description ：
@Author      ：Hello World
@Date        ：2025/8/27 下午6:16 
'''
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
import torch
from datasets import load_dataset

# 1. 加载基础模型
model_name = "facebook/opt-125m"  # 一个小型模型用于演示
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print(f"原始模型参数量: {model.num_parameters():,}")

# 2. 配置LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,  # 因果语言模型
    inference_mode=False,
    r=8,           # 秩（rank）
    lora_alpha=32,  # 缩放参数
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"]  # 要适配的模块
)

# 3. 应用LoRA
peft_model = get_peft_model(model, lora_config)
print(f"LoRA可训练参数量: {peft_model.num_parameters():,}")
print(f"可训练参数占比: {peft_model.num_parameters() / model.num_parameters() * 100:.2f}%")

# 4. 准备训练数据（简化示例）
def prepare_dataset():
    # 实际使用时可以从huggingface datasets加载
    texts = [
        "Translate to French: Hello world → Bonjour le monde",
        "Translate to French: I love AI → J'adore l'IA",
        "Translate to French: Good morning → Bonjour"
    ]
    return texts

# 5. 训练配置
training_args = TrainingArguments(
    output_dir="./lora_results",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=3e-4,
    num_train_epochs=1,
    logging_steps=10,
    save_steps=100,
    fp16=True  # 混合精度训练
)

print("✅ LoRA模型准备完成！")

# 实际训练代码会在这里，但需要更多数据和计算资源
# trainer = Trainer(model=peft_model, args=training_args, train_dataset=dataset)
# trainer.train()