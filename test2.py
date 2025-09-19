# %% [Step 0] 导入库 + 路径设置
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict, Counter
from tqdm import tqdm
import os
import gc
import json

# 数据路径
DATA_DIR = '/kaggle/input/otto-recommender-system'
TRAIN_PATH = os.path.join(DATA_DIR, 'train.jsonl')
TEST_PATH = os.path.join(DATA_DIR, 'test.jsonl')
SAMPLE_SUB_PATH = os.path.join(DATA_DIR, 'sample_submission.csv')

print("✅ Libraries imported and paths set.")


# %% [Step 1] 内存安全加载 + 预处理（流式处理）

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


# 测试：只加载 1000 个 sessions
train_session_data, train_session_stats = load_and_preprocess_data_streaming(
    TRAIN_PATH,
    max_events_per_session=30,
    sample_n_sessions=1000  # 仅测试用
)

# 测试数据（全量加载）
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


# %% [Step 2] 优化版 Dataset —— 预处理缓存（大幅降低 CPU 负载）
class OttoDataset(Dataset):
    def __init__(self, session_data, aid_to_idx, max_len=30, is_test=False):
        self.session_ids = list(session_data.keys())
        self.is_test = is_test
        self.max_len = max_len

        # 预处理并缓存所有数据
        self.cached_data = []
        desc = f"Preprocessing {'test' if is_test else 'train'} dataset"
        for session_id in tqdm(self.session_ids, desc=desc):
            data = session_data[session_id]
            aids = data['aids']

            # 映射 + padding
            aid_indices = [aid_to_idx.get(aid, 0) for aid in aids]
            if len(aid_indices) < max_len:
                aid_indices = [0] * (max_len - len(aid_indices)) + aid_indices
            else:
                aid_indices = aid_indices[-max_len:]

            user_group = int(data['user_group'])

            # 转为 tensor（CPU 上预处理）
            aid_tensor = torch.tensor(aid_indices, dtype=torch.long)
            user_tensor = torch.tensor(user_group, dtype=torch.long)

            if is_test:
                # 确保 session_id 是 int（适配 submission 格式）
                self.cached_data.append((aid_tensor, user_tensor, int(session_id)))
            else:
                self.cached_data.append((aid_tensor, user_tensor))

    def __len__(self):
        return len(self.cached_data)

    def __getitem__(self, idx):
        return self.cached_data[idx]  # 直接返回缓存，无计算！


# 构建词表
all_aids = set()
for data in list(train_session_data.values()) + list(test_session_data.values()):
    all_aids.update(data['aids'])

aid_to_idx = {aid: idx + 1 for idx, aid in enumerate(all_aids)}  # 0 为 padding
idx_to_aid = {idx: aid for aid, idx in aid_to_idx.items()}

print(f"✅ Vocabulary size: {len(aid_to_idx)}")

# 创建 Dataset（预处理缓存）
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

        # Task Embedding
        self.task_embedding = nn.Embedding(3, task_emb_dim)  # 3 类用户

        # 路由网络
        self.task_router = nn.Linear(task_emb_dim, num_experts)

        # 专家网络
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(input_dim, expert_hidden_dim),
                nn.ReLU(),
                nn.Linear(expert_hidden_dim, input_dim)
            ) for _ in range(num_experts)
        ])

    def forward(self, x, task_ids):
        task_emb = self.task_embedding(task_ids)  # [B, T]
        logits = self.task_router(task_emb)  # [B, N]
        weights = torch.softmax(logits, dim=1)  # [B, N]

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

        self.aid_embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.pos_embedding = nn.Embedding(max_len, embed_dim)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=embed_dim * 4,
            batch_first=True,
            dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.moe = TaskBasedMoE(num_experts=num_experts, input_dim=embed_dim, task_emb_dim=16)
        self.output_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, aid_seq, user_group):
        B, L = aid_seq.shape
        x = self.aid_embedding(aid_seq)  # [B, L, D]
        pos = torch.arange(L, device=aid_seq.device).unsqueeze(0).expand(B, -1)
        x = x + self.pos_embedding(pos)
        x = self.transformer(x)  # [B, L, D]
        x = x[:, -1, :]  # [B, D]
        x = self.moe(x, user_group)  # [B, D]
        x = self.output_proj(x)
        return x


# 初始化模型
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


# %% [Step 4] 真实训练：Sampled Softmax Loss + 优化 DataLoader

class NegativeSampler:
    def __init__(self, vocab_size, num_negatives=5):
        self.vocab_size = vocab_size
        self.num_negatives = num_negatives

    def sample(self, batch_size):
        return torch.randint(1, self.vocab_size, (batch_size, self.num_negatives))


sampler = NegativeSampler(vocab_size=len(aid_to_idx) + 1, num_negatives=5)

# ✅ 优化 DataLoader：多进程 + 锁页内存
train_loader = DataLoader(
    train_dataset,
    batch_size=128,  # 增大 batch_size 提升 GPU 利用率
    shuffle=True,
    num_workers=2,  # Kaggle 通常 2~4 核，设 2 安全
    pin_memory=True,  # 加速 CPU→GPU 传输
    prefetch_factor=2  # 预取
)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

model.train()
print("✅ Starting REAL training (1 epoch)...")

for epoch in range(1):
    total_loss = 0
    for batch_idx, (aid_seq, user_group) in enumerate(train_loader):
        # ✅ non_blocking=True 加速数据传输
        aid_seq = aid_seq.to(device, non_blocking=True)
        user_group = user_group.to(device, non_blocking=True)

        optimizer.zero_grad()

        session_emb = model(aid_seq, user_group)  # [B, D]
        target_aid_indices = aid_seq[:, -1]  # [B] 最后一个商品为正样本

        neg_samples = sampler.sample(aid_seq.size(0)).to(device)  # [B, N_neg]
        all_embeddings = model.aid_embedding.weight  # [V, D]

        pos_emb = all_embeddings[target_aid_indices]  # [B, D]
        neg_emb = all_embeddings[neg_samples]  # [B, N_neg, D]

        pos_logits = torch.sum(session_emb * pos_emb, dim=1, keepdim=True)  # [B, 1]
        neg_logits = torch.bmm(neg_emb, session_emb.unsqueeze(2)).squeeze(2)  # [B, N_neg]

        logits = torch.cat([pos_logits, neg_logits], dim=1)  # [B, 1+N_neg]
        labels = torch.zeros(aid_seq.size(0), dtype=torch.long).to(device)  # [B]

        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        if batch_idx % 10 == 0:
            print(f"Batch {batch_idx}, Real Loss: {loss.item():.4f}")

    print(f"Epoch {epoch + 1} Average Real Loss: {total_loss / (batch_idx + 1):.4f}")

print("✅ REAL Training loop completed.")


# %% [Step 5] 生成推荐 + 优化 DataLoader

def generate_recommendations(model, test_loader, idx_to_aid, device, top_k=20):
    model.eval()
    session_preds = {}

    aid_embeddings = model.aid_embedding.weight[1:].detach().to(device)  # [V, D]
    print(f"✅ Item embeddings shape: {aid_embeddings.shape}")

    with torch.no_grad():
        for batch in tqdm(test_loader, desc="Generating recommendations"):
            if len(batch) == 3:
                aid_seq, user_group, session_ids = batch
            else:
                aid_seq, user_group = batch
                session_ids = [0] * len(aid_seq)

            # ✅ non_blocking=True
            aid_seq = aid_seq.to(device, non_blocking=True)
            user_group = user_group.to(device, non_blocking=True)

            session_emb = model(aid_seq, user_group)  # [B, D]
            scores = torch.matmul(session_emb, aid_embeddings.T)  # [B, V]

            top_scores, top_indices = torch.topk(scores, min(top_k, scores.shape[1]), dim=1)

            for i, session_id in enumerate(session_ids):
                pred_aids = []
                for idx in top_indices[i]:
                    aid_idx = idx.item() + 1
                    if aid_idx in idx_to_aid:
                        pred_aids.append(idx_to_aid[aid_idx])
                    if len(pred_aids) >= top_k:
                        break
                session_preds[session_id] = pred_aids[:top_k]

    return session_preds


# ✅ 优化测试 DataLoader
test_loader_full = DataLoader(
    test_dataset,
    batch_size=128,
    num_workers=2,
    pin_memory=True,
    shuffle=False
)

session_preds = generate_recommendations(model, test_loader_full, idx_to_aid, device, top_k=20)

print("\n--- Sample Predictions ---")
for i, (sid, aids) in enumerate(list(session_preds.items())[:5]):
    print(f"Session {sid}: {aids[:5]}...")

print(f"✅ Total sessions predicted: {len(session_preds)}")

# %% [Step 6] 生成三种类型预测
pred_df_clicks = pd.DataFrame({
    'session_type': [f"{sid}_clicks" for sid in session_preds.keys()],
    'labels': [" ".join(map(str, aids)) for aids in session_preds.values()]
})

pred_df_carts = pd.DataFrame({
    'session_type': [f"{sid}_carts" for sid in session_preds.keys()],
    'labels': [" ".join(map(str, aids)) for aids in session_preds.values()]
})

pred_df_orders = pd.DataFrame({
    'session_type': [f"{sid}_orders" for sid in session_preds.keys()],
    'labels': [" ".join(map(str, aids)) for aids in session_preds.values()]
})

submission_df = pd.concat([pred_df_clicks, pred_df_carts, pred_df_orders], ignore_index=True)
print("✅ Submission DataFrame created.")
print(submission_df.head(6))

# %% [Step 7] 保存提交文件
submission_df.to_csv("submission_transformer_moe.csv", index=False)
print(f"✅ Submission saved to 'submission_transformer_moe.csv'")
print(f"Submission shape: {submission_df.shape}")

# 验证格式
sample_sub = pd.read_csv(SAMPLE_SUB_PATH)
print(f"\nSample submission shape: {sample_sub.shape}")
print("Columns match:", list(submission_df.columns) == list(sample_sub.columns))