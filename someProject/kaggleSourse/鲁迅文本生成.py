#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：鲁迅文本生成.py
@Description ：
@Author      ：Hello World
@Date        ：2025/10/28 下午2:28 
'''
import os
import math
import json
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.nn import functional as F
from tqdm import tqdm
from transformers import get_linear_schedule_with_warmup
from torch.optim import AdamW

# ---------------------------
# 配置参数
# ---------------------------
TRAIN_CSV = "/kaggle/input/scale-lab-25-project-3-llm/train.csv"
TEST_CSV = "/kaggle/input/scale-lab-25-project-3-llm/test.csv"
MODEL_DIR = "/kaggle/working/model4"

MAX_SEQ_LEN = 512
BATCH_SIZE = 8
EPOCHS = 15
LR = 5e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 梯度累积和 warmup
GRAD_ACCUM_STEPS = 4
WARMUP_STEPS = 100

# 生成参数
TOP_K = 50
TOP_P = 0.95
TEMPERATURE = 1.0
MAX_NEW_TOKENS = 200
NO_REPEAT_NGRAM_SIZE = 3

os.makedirs(MODEL_DIR, exist_ok=True)

# ---------------------------
# 加载数据
# ---------------------------
train_df = pd.read_csv(TRAIN_CSV)
test_df = pd.read_csv(TEST_CSV)

train_texts = train_df["context"].tolist()
test_texts = test_df["context"].tolist()

# ---------------------------
# 构建字符级 tokenizer
# ---------------------------
all_text = "".join(train_texts)
chars = sorted(list(set(all_text)))
vocab_size = len(chars)
print("Vocab size:", vocab_size)

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for ch, i in stoi.items()}

def encode(text):
    return [stoi.get(c, 0) for c in text]

def decode(ids):
    return "".join([itos[i] for i in ids])

# ---------------------------
# 保存 / 加载 tokenizer
# ---------------------------
def save_tokenizer(stoi, itos, path):
    tok = {"stoi": stoi, "itos": itos}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tok, f, ensure_ascii=False, indent=2)

def load_tokenizer(path):
    with open(path, "r", encoding="utf-8") as f:
        tok = json.load(f)
    return tok["stoi"], tok["itos"]

# ---------------------------
# 保存 / 加载 config
# ---------------------------
def save_config(config, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------
# Dataset
# ---------------------------
class CharDataset(Dataset):
    def __init__(self, texts, seq_len=MAX_SEQ_LEN):
        self.data = []
        for t in texts:
            ids = encode(t)
            for i in range(0, len(ids) - seq_len, seq_len):
                self.data.append(torch.tensor(ids[i:i+seq_len], dtype=torch.long))
        self.data = self.data if self.data else [torch.tensor(encode(t), dtype=torch.long) for t in texts]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx][:-1]
        y = self.data[idx][1:]
        return x, y

train_dataset = CharDataset(train_texts)
test_dataset = CharDataset(test_texts)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

# ---------------------------
# Transformer 模型
# ---------------------------
class TransformerBlock(nn.Module):
    def __init__(self, hidden, heads, ff_hidden, dropout):
        super().__init__()
        self.attn = nn.MultiheadAttention(hidden, heads, dropout=dropout)
        self.ln1 = nn.LayerNorm(hidden)
        self.ff = nn.Sequential(
            nn.Linear(hidden, ff_hidden),
            nn.ReLU(),
            nn.Linear(ff_hidden, hidden)
        )
        self.ln2 = nn.LayerNorm(hidden)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        attn_out, _ = self.attn(x, x, x)
        x = self.ln1(x + self.dropout(attn_out))
        ff_out = self.ff(x)
        x = self.ln2(x + self.dropout(ff_out))
        return x

class CharTransformer(nn.Module):
    def __init__(self, vocab_size, hidden=512, n_layers=6, n_heads=8, seq_len=MAX_SEQ_LEN, dropout=0.1):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, hidden)
        self.pos_emb = nn.Embedding(seq_len, hidden)
        self.layers = nn.ModuleList([TransformerBlock(hidden, n_heads, hidden*4, dropout) for _ in range(n_layers)])
        self.ln_f = nn.LayerNorm(hidden)
        self.head = nn.Linear(hidden, vocab_size, bias=False)
        self.seq_len = seq_len

    def forward(self, x):
        B, T = x.shape
        tok_emb = self.token_emb(x)
        pos = torch.arange(T, device=x.device).unsqueeze(0).expand(B, T)
        pos_emb = self.pos_emb(pos)
        h = tok_emb + pos_emb
        h = h.transpose(0, 1)  # [T,B,H] for MultiheadAttention
        for layer in self.layers:
            h = layer(h)
        h = h.transpose(0, 1)  # back to [B,T,H]
        h = self.ln_f(h)
        logits = self.head(h)
        return logits

# ---------------------------
# 参数统计
# ---------------------------
def count_parameters(model):
    return sum(p.numel() for p in model.parameters())

# ---------------------------
# 训练函数
# ---------------------------
def train_model(model, train_loader, test_loader, epochs, lr, device, config):
    optimizer = AdamW(model.parameters(), lr=lr)
    total_steps = epochs * len(train_loader) // GRAD_ACCUM_STEPS
    scheduler = get_linear_schedule_with_warmup(optimizer, WARMUP_STEPS, total_steps)
    scaler = torch.cuda.amp.GradScaler(enabled=True)
    model.to(device)

    best_ppl = float("inf")
    loss_fn = nn.CrossEntropyLoss()

    # 保存 tokenizer & config（只保存一次）
    save_tokenizer(stoi, itos, os.path.join(MODEL_DIR, "tokenizer.json"))
    save_config(config, os.path.join(MODEL_DIR, "config.json"))

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        optimizer.zero_grad()
        for step, (x, y) in enumerate(tqdm(train_loader, desc=f"Epoch {epoch+1}")):
            x, y = x.to(device), y.to(device)
            with torch.cuda.amp.autocast(enabled=True):
                logits = model(x)
                loss = loss_fn(logits.view(-1, logits.size(-1)), y.view(-1))
            scaler.scale(loss / GRAD_ACCUM_STEPS).backward()
            total_loss += loss.item() * x.size(0)

            if (step + 1) % GRAD_ACCUM_STEPS == 0:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
                scheduler.step()

        avg_loss = total_loss / len(train_loader.dataset)
        ppl = math.exp(avg_loss)
        print(f"Epoch {epoch+1} | Train PPL={ppl:.4f}")

        # 评估
        model.eval()
        total_loss_eval = 0
        with torch.no_grad():
            for x, y in test_loader:
                x, y = x.to(device), y.to(device)
                logits = model(x)
                loss = loss_fn(logits.view(-1, logits.size(-1)), y.view(-1))
                total_loss_eval += loss.item() * x.size(0)
        avg_loss_eval = total_loss_eval / len(test_loader.dataset)
        ppl_eval = math.exp(avg_loss_eval)
        print(f"Eval PPL={ppl_eval:.4f}")

        # 保存模型
        torch.save(model.state_dict(), os.path.join(MODEL_DIR, f"epoch{epoch+1}.pt"))
        if ppl_eval < best_ppl:
            best_ppl = ppl_eval
            torch.save(model.state_dict(), os.path.join(MODEL_DIR, "best_model.pt"))
            print("Saved new best model!")

# ---------------------------
# 推理相关函数
# ---------------------------
def load_model_for_inference(model_dir, device="cpu"):
    config = load_config(os.path.join(model_dir, "config.json"))
    stoi, itos = load_tokenizer(os.path.join(model_dir, "tokenizer.json"))

    model = CharTransformer(**config)
    model.load_state_dict(torch.load(os.path.join(model_dir, "best_model.pt"), map_location=device))
    model.to(device)
    model.eval()
    return model, stoi, itos

def generate_text(model, stoi, itos, prompt, max_new_tokens=200, temperature=1.0, top_k=50, top_p=0.95):
    model.eval()
    input_ids = torch.tensor([stoi.get(c,0) for c in prompt], dtype=torch.long).unsqueeze(0).to(next(model.parameters()).device)
    generated = input_ids.tolist()[0]

    for _ in range(max_new_tokens):
        logits = model(input_ids)[:, -1, :]
        logits = logits / temperature

        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        sorted_indices_to_remove = cumulative_probs > top_p
        if top_k > 0:
            sorted_indices_to_remove[..., top_k:] = True
        for batch_idx in range(logits.size(0)):
            logits[batch_idx, sorted_indices[batch_idx][sorted_indices_to_remove[batch_idx]]] = -float("Inf")

        probs = F.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1).item()

        generated.append(next_id)
        input_ids = torch.tensor([generated], dtype=torch.long).to(next(model.parameters()).device)

    return "".join([itos[i] for i in generated])

# ---------------------------
# 主程序入口
# ---------------------------
config = {
    "vocab_size": vocab_size,
    "hidden": 512,
    "n_layers": 6,
    "n_heads": 8,
    "seq_len": MAX_SEQ_LEN,
    "dropout": 0.1
}

model = CharTransformer(**config)
print(f"模型总参数量: {count_parameters(model)/1e6:.2f} M")

train_model(model, train_loader, test_loader, EPOCHS, LR, DEVICE, config)

# 推理示例
# model, stoi, itos = load_model_for_inference(MODEL_DIR, DEVICE)
# print(generate_text(model, stoi, itos, "鲁迅", max_new_tokens=200))