#%% [Step 0] 导入库 + 路径设置
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict, Counter
from tqdm import tqdm
import os
import gc

# 数据路径
DATA_DIR = '/kaggle/input/otto-recommender-system'
TRAIN_PATH = os.path.join(DATA_DIR, 'train.jsonl')
TEST_PATH = os.path.join(DATA_DIR, 'test.jsonl')
SAMPLE_SUB_PATH = os.path.join(DATA_DIR, 'sample_submission.csv')

print("✅ Libraries imported and paths set.")
# %% [Step 1] 内存安全加载 + 预处理（流式处理）
import json
from collections import defaultdict


def load_and_preprocess_data_streaming(filepath, max_events_per_session=30, sample_n_sessions=None):
    print(f"Loading {filepath} in streaming mode...")

    session_data = {}  # {session_id: { 'aids': [], 'types': [], 'ts': [], 'user_group': None }}
    session_stats = {}  # {session_id: stats_dict}

    with open(filepath, 'r') as f:
        lines = f.readlines()
        if sample_n_sessions:
            lines = lines[:sample_n_sessions]  # 仅用于测试

        for line_idx, line in enumerate(tqdm(lines, desc="Processing sessions")):
            row = json.loads(line)
            session_id = row['session']
            events = row['events']

            # 只保留最后 max_events_per_session 个事件
            events = events[-max_events_per_session:]

            aids = [e['aid'] for e in events]
            types = [e['type'] for e in events]
            tss = [e['ts'] for e in events]

            # 计算统计特征
            session_length = len(events)
            click_count = types.count('clicks')
            cart_count = types.count('carts')
            order_count = types.count('orders')

            # 定义用户分群（Task ID）
            if session_length <= 3:
                user_group = 0  # 新用户 / 低活跃
            elif order_count > 0:
                user_group = 2  # 付费用户
            else:
                user_group = 1  # 活跃非付费

            # 存储（只存必要信息）
            session_data[session_id] = {
                'aids': aids,
                'types': types,
                'ts': tss,
                'user_group': user_group
            }

            session_stats[session_id] = {
                'session_length': session_length,
                'click_count': click_count,
                'cart_count': cart_count,
                'order_count': order_count,
                'user_group': user_group
            }

            # 如果只是测试，限制 session 数量
            if sample_n_sessions and len(session_data) >= sample_n_sessions:
                break

    print(f"✅ Loaded {len(session_data)} sessions from {filepath}")
    return session_data, session_stats


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ⚠️ 重要：训练时不要加载全部数据！先用小样本测试流程
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 测试：只加载 1000 个 sessions
train_session_data, train_session_stats = load_and_preprocess_data_streaming(
    TRAIN_PATH,
    max_events_per_session=30,
    sample_n_sessions=1000  # 仅测试用，正式训练可设为 None 或 100000
)

# 测试数据（全量加载，因为只有 400MB）
test_session_data, test_session_stats = load_and_preprocess_data_streaming(
    TEST_PATH,
    max_events_per_session=30
)

# 打印测试
print("\n--- Train Sample ---")
sample_sid = list(train_session_data.keys())[0]
print(f"Session {sample_sid}:")
print(f"  AIDs: {train_session_data[sample_sid]['aids'][:5]}...")
print(f"  Types: {train_session_data[sample_sid]['types'][:5]}")
print(f"  User Group: {train_session_data[sample_sid]['user_group']}")

print(f"\nTotal train sessions loaded: {len(train_session_data)}")
print(f"User group distribution (train):")
train_groups = [s['user_group'] for s in train_session_stats.values()]
print(pd.Series(train_groups).value_counts())

print("\n--- Test Sample ---")
sample_sid = list(test_session_data.keys())[0]
print(f"Session {sample_sid}:")
print(f"  AIDs: {test_session_data[sample_sid]['aids'][:5]}...")
print(f"  User Group: {test_session_data[sample_sid]['user_group']}")

print(f"\nTotal test sessions loaded: {len(test_session_data)}")
print(f"User group distribution (test):")
test_groups = [s['user_group'] for s in test_session_stats.values()]
print(pd.Series(test_groups).value_counts())


# %% [Step 2] 构建 Dataset（适配新数据结构）
class OttoDataset(Dataset):
    def __init__(self, session_data, aid_to_idx, max_len=30, is_test=False):
        self.session_ids = list(session_data.keys())
        self.session_data = session_data
        self.aid_to_idx = aid_to_idx
        self.max_len = max_len
        self.is_test = is_test

    def __len__(self):
        return len(self.session_ids)

    def __getitem__(self, idx):
        session_id = self.session_ids[idx]
        data = self.session_data[session_id]

        # 商品序列（转为 index）
        aids = data['aids']
        aid_indices = [self.aid_to_idx.get(aid, 0) for aid in aids]  # 0 为 UNK

        # 补齐/截断
        if len(aid_indices) < self.max_len:
            aid_indices = [0] * (self.max_len - len(aid_indices)) + aid_indices
        else:
            aid_indices = aid_indices[-self.max_len:]

        # 用户分群（Task ID）
        user_group = int(data['user_group'])

        if self.is_test:
            return torch.tensor(aid_indices, dtype=torch.long), torch.tensor(user_group, dtype=torch.long), session_id
        else:
            return torch.tensor(aid_indices, dtype=torch.long), torch.tensor(user_group, dtype=torch.long)


# 构建词表（基于训练+测试数据）
all_aids = set()
for data in list(train_session_data.values()) + list(test_session_data.values()):
    all_aids.update(data['aids'])

aid_to_idx = {aid: idx + 1 for idx, aid in enumerate(all_aids)}  # 0 为 padding
idx_to_aid = {idx: aid for aid, idx in aid_to_idx.items()}

print(f"✅ Vocabulary size: {len(aid_to_idx)}")

# 创建 Dataset
train_dataset = OttoDataset(train_session_data, aid_to_idx, max_len=20)
test_dataset = OttoDataset(test_session_data, aid_to_idx, max_len=20, is_test=True)

# 测试 Dataset
print("\n--- Testing OttoDataset ---")
sample_aid_seq, sample_user_group, sample_sid = test_dataset[0]
print(f"Sample aid_seq: {sample_aid_seq}")
print(f"Sample user_group: {sample_user_group}")
print(f"Sample session_id: {sample_sid}")
print(f"Dataset length: {len(test_dataset)}")


# %% [Step 3] 构建模型
class TaskBasedMoE(nn.Module):
    def __init__(self, num_experts, input_dim, task_emb_dim, expert_hidden_dim=256):
        super().__init__()
        self.num_experts = num_experts

        # Task Embedding（用户分群 → 向量）
        self.task_embedding = nn.Embedding(3, task_emb_dim)  # 3 类用户

        # 路由网络：task_emb → 专家权重
        self.task_router = nn.Linear(task_emb_dim, num_experts)

        # 专家网络（每个专家是一个 FFN）
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(input_dim, expert_hidden_dim),
                nn.ReLU(),
                nn.Linear(expert_hidden_dim, input_dim)
            ) for _ in range(num_experts)
        ])

    def forward(self, x, task_ids):
        # x: [B, D]
        task_emb = self.task_embedding(task_ids)  # [B, T]
        logits = self.task_router(task_emb)  # [B, N]
        weights = torch.softmax(logits, dim=1)  # [B, N]

        # 加权融合专家输出
        out = torch.zeros_like(x)
        for i in range(self.num_experts):
            expert_out = self.experts[i](x)
            out += weights[:, i].unsqueeze(1) * expert_out

        return out


class OttoTransformer(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, num_heads=4, num_layers=2, num_experts=3, max_len=30):
        super().__init__()
        self.embed_dim = embed_dim
        self.max_len = max_len

        # 商品 Embedding
        self.aid_embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)

        # Positional Encoding
        self.pos_embedding = nn.Embedding(max_len, embed_dim)

        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=embed_dim * 4,
            batch_first=True,
            dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # Task-based MoE
        self.moe = TaskBasedMoE(
            num_experts=num_experts,
            input_dim=embed_dim,
            task_emb_dim=16
        )

        # 输出层
        self.output_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, aid_seq, user_group):
        B, L = aid_seq.shape

        # Embedding + Position
        x = self.aid_embedding(aid_seq)  # [B, L, D]
        pos = torch.arange(L, device=aid_seq.device).unsqueeze(0).expand(B, -1)
        x = x + self.pos_embedding(pos)

        # Transformer
        x = self.transformer(x)  # [B, L, D]

        # 取最后一个时间步
        x = x[:, -1, :]  # [B, D]

        # Task-based MoE
        x = self.moe(x, user_group)  # [B, D]

        # 输出
        x = self.output_proj(x)
        return x


# 测试模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = OttoTransformer(
    vocab_size=len(aid_to_idx) + 1,
    embed_dim=64,
    num_experts=3,
    num_layers=2
).to(device)

print("✅ Model created.")

# 测试前向传播
test_loader = DataLoader(test_dataset, batch_size=4, shuffle=False)
aid_seq, user_group, _ = next(iter(test_loader))
aid_seq = aid_seq.to(device)
user_group = user_group.to(device)

with torch.no_grad():
    output = model(aid_seq, user_group)
    print(f"✅ Forward pass successful. Output shape: {output.shape}")


# %% [Step 4] 真实训练：Sampled Softmax Loss

# 负采样器（简单版本：随机采样）
class NegativeSampler:
    def __init__(self, vocab_size, num_negatives=5):
        self.vocab_size = vocab_size
        self.num_negatives = num_negatives

    def sample(self, batch_size):
        # [B, N_neg]
        return torch.randint(1, self.vocab_size, (batch_size, self.num_negatives))


# 初始化负采样器
sampler = NegativeSampler(vocab_size=len(aid_to_idx) + 1, num_negatives=5)

# 使用真实训练集
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 优化器
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# 损失函数
criterion = nn.CrossEntropyLoss()

model.train()
print("✅ Starting REAL training (1 epoch)...")

for epoch in range(1):
    total_loss = 0
    for batch_idx, (aid_seq, user_group) in enumerate(train_loader):
        aid_seq = aid_seq.to(device)
        user_group = user_group.to(device)

        optimizer.zero_grad()

        # 获取 session 表征
        session_emb = model(aid_seq, user_group)  # [B, D]

        # 目标：预测序列中最后一个 aid（作为正样本）
        # 注意：我们输入的是最后30个事件，目标可以是最后一个 aid
        target_aid_indices = aid_seq[:, -1]  # [B] —— 最后一个商品作为正样本

        # 负采样
        neg_samples = sampler.sample(aid_seq.size(0)).to(device)  # [B, N_neg]

        # 获取商品 Embedding（包括正样本和负样本）
        all_embeddings = model.aid_embedding.weight  # [V, D]

        # 正样本 embedding
        pos_emb = all_embeddings[target_aid_indices]  # [B, D]

        # 负样本 embedding
        neg_emb = all_embeddings[neg_samples]  # [B, N_neg, D]

        # 计算 logits
        pos_logits = torch.sum(session_emb * pos_emb, dim=1, keepdim=True)  # [B, 1]
        neg_logits = torch.bmm(neg_emb, session_emb.unsqueeze(2)).squeeze(2)  # [B, N_neg]

        # 合并 logits
        logits = torch.cat([pos_logits, neg_logits], dim=1)  # [B, 1 + N_neg]

        # 标签：正样本在位置 0
        labels = torch.zeros(aid_seq.size(0), dtype=torch.long).to(device)  # [B]

        # 计算损失
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        if batch_idx % 10 == 0:
            print(f"Batch {batch_idx}, Real Loss: {loss.item():.4f}")

    print(f"Epoch {epoch + 1} Average Real Loss: {total_loss / (batch_idx + 1):.4f}")

print("✅ REAL Training loop completed.")


# %% [Step 5] 生成推荐
def generate_recommendations(model, test_loader, idx_to_aid, device, top_k=20):
    model.eval()
    session_preds = {}

    # 提取商品 Embedding（排除 padding）
    aid_embeddings = model.aid_embedding.weight[1:].detach().to(device)  # [V, D]
    print(f"✅ Item embeddings shape: {aid_embeddings.shape}")

    with torch.no_grad():
        for batch in tqdm(test_loader, desc="Generating recommendations"):
            if len(batch) == 3:
                aid_seq, user_group, session_ids = batch
            else:
                aid_seq, user_group = batch
                session_ids = [0] * len(aid_seq)  # dummy

            aid_seq = aid_seq.to(device)
            user_group = user_group.to(device)

            # 获取 session 表征
            session_emb = model(aid_seq, user_group)  # [B, D]

            # 计算与所有商品的相似度（点积）
            scores = torch.matmul(session_emb, aid_embeddings.T)  # [B, V]

            # 取 top-K
            top_scores, top_indices = torch.topk(scores, min(top_k, scores.shape[1]), dim=1)

            for i, session_id in enumerate(session_ids):
                pred_aids = []
                for idx in top_indices[i]:
                    aid_idx = idx.item() + 1  # 因为去掉了 padding 0
                    if aid_idx in idx_to_aid:
                        pred_aids.append(idx_to_aid[aid_idx])
                    if len(pred_aids) >= top_k:
                        break
                session_preds[session_id] = pred_aids[:top_k]

    return session_preds


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ✅ 修复：使用 test_session_data 而不是 test_df
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
full_test_dataset = OttoDataset(test_session_data, aid_to_idx, max_len=20, is_test=True)
test_loader_full = DataLoader(full_test_dataset, batch_size=128, shuffle=False)

# 生成推荐
session_preds = generate_recommendations(model, test_loader_full, idx_to_aid, device, top_k=20)

# 测试输出
print("\n--- Sample Predictions ---")
for i, (sid, aids) in enumerate(list(session_preds.items())[:5]):
    print(f"Session {sid}: {aids[:5]}...")

print(f"✅ Total sessions predicted: {len(session_preds)}")