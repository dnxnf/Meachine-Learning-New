# %% [Step 0] CONFIG + Imports & paths
print("start")
import os
import json
import evaluate_enhanced_metrics
import gc
from collections import defaultdict, Counter

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from transformers import get_linear_schedule_with_warmup

# ✅ 所有参数集中在这里，方便调试
CONFIG = {
    # 数据相关
    'sample_n_sessions': 30000,  # 训练数据量
    'val_sample_n_sessions': 6000,  # 验证数据量
    'eval_sample_n_sessions': 2000,  # 可调整：评估多少个 validation sessions
    'max_events_per_session': 30,
    'max_seq_len': 20,  # 序列最大长度
    'cache_dir': "/kaggle/working/cache",

    # 模型结构
    'embed_dim': 64,
    'num_heads': 4,
    'num_layers': 2,
    'num_experts': 3,
    'expert_hidden_dim': 256,
    'task_emb_dim': 32,
    'dropout': 0.1,
    'max_capacity': 128,  # 增加容量，避免拥堵
    'coda_lambda': 0.3,
    'temperature': 0.1,

    # 训练参数
    'batch_size': 512,
    'num_workers': 0,
    'epochs': 3,
    'learning_rate': 1e-3,  # 更稳定的学习率
    'weight_decay': 0.01,
    'grad_clip': 1.0,
    'warmup_ratio': 0.2,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',

    # 负采样
    'num_negatives': 100,

    # 评估
    'top_k_list': [20, 50],
}

# You may adjust these paths if needed
DATA_DIR = '/kaggle/input/otto-recommender-system'
TRAIN_PATH = os.path.join(DATA_DIR, 'train.jsonl')
TEST_PATH = os.path.join(DATA_DIR, 'test.jsonl')
SAMPLE_SUB_PATH = os.path.join(DATA_DIR, 'sample_submission.csv')

print("✅ Libraries imported and paths set.")


# %% [Step 1] Streaming loader + caching

def collate_train(batch):
    for i, item in enumerate(batch):
        if item is None:
            raise ValueError(f"Found None at batch index {i}")
        if len(item) != 5:
            raise ValueError(f"Item at index {i} has {len(item)} elements, expected 5")
    try:
        aid_tensors, type_tensors, ts_tensors, user_tensors, gts = zip(*batch)
        aid_tensors = torch.stack(aid_tensors, dim=0)
        type_tensors = torch.stack(type_tensors, dim=0)
        ts_tensors = torch.stack(ts_tensors, dim=0)
        user_tensors = torch.stack(user_tensors, dim=0)
        return aid_tensors, type_tensors, ts_tensors, user_tensors, list(gts)
    except Exception as e:
        print(f"❌ Collate error: {e}")
        print(f"First item: {batch[0] if len(batch) > 0 else 'empty'}")
        raise


def collate_test(batch):
    aid_tensors, type_tensors, ts_tensors, user_tensors, session_ids = zip(*batch)
    aid_tensors = torch.stack(aid_tensors, dim=0)
    type_tensors = torch.stack(type_tensors, dim=0)
    ts_tensors = torch.stack(ts_tensors, dim=0)
    user_tensors = torch.stack(user_tensors, dim=0)
    return aid_tensors, type_tensors, ts_tensors, user_tensors, list(session_ids)


def load_and_preprocess_data_streaming(filepath, max_events_per_session=30, sample_n_sessions=None, is_test=False):
    cache_dir = CONFIG['cache_dir']
    os.makedirs(cache_dir, exist_ok=True)
    filename = os.path.basename(filepath).replace('.jsonl', '')
    cache_name = f"{filename}_sessions{sample_n_sessions or 'all'}_len{max_events_per_session}.pkl"
    cache_path = os.path.join(cache_dir, cache_name)
    if os.path.exists(cache_path):
        print(f"📂 Loading from cache: {cache_path}")
        with open(cache_path, 'rb') as f:
            return pickle.load(f)

    print(f"Streaming read {filepath} ...")
    session_data = {}
    session_stats = {}
    ground_truth = {}
    type_map = {
        'clicks': 0,
        'carts': 1,
        'orders': 2
    }

    with open(filepath, 'r') as f:
        for line_idx, line in enumerate(tqdm(f, desc="Processing sessions")):
            if sample_n_sessions and line_idx >= sample_n_sessions:
                break
            row = json.loads(line)
            session_id = row['session']
            events = row['events'][-max_events_per_session:]

            aids = [e['aid'] for e in events]
            types = [type_map[e['type']] for e in events]
            tss = [e['ts'] for e in events]

            session_length = len(events)
            click_count = types.count(0)
            cart_count = types.count(1)
            order_count = types.count(2)

            if session_length <= 3:
                user_group = 0
            elif order_count > 0:
                user_group = 2
            else:
                user_group = 1

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

            if not is_test:
                gt = {
                    'clicks': [],
                    'carts': [],
                    'orders': []
                }
                for aid, typ in zip(aids, [e['type'] for e in events]):
                    gt[typ].append(aid)
                ground_truth[session_id] = gt

    print(f"✅ Loaded {len(session_data)} sessions from {filepath}")
    with open(cache_path, 'wb') as f:
        pickle.dump((session_data, session_stats, ground_truth), f)
    print(f"💾 Saved to cache: {cache_path}")
    return session_data, session_stats, ground_truth


# 🧹 清除缓存
# !rm -rf /kaggle/working/cache/*
print("🧹 Cache cleared. Will regenerate data.")

# Load data
train_session_data, train_session_stats, train_ground_truth = load_and_preprocess_data_streaming(
    TRAIN_PATH,
    max_events_per_session=CONFIG['max_events_per_session'],
    sample_n_sessions=CONFIG['sample_n_sessions'],
    is_test=False
)
test_session_data, test_session_stats, _ = load_and_preprocess_data_streaming(
    TEST_PATH,
    max_events_per_session=CONFIG['max_events_per_session'],
    is_test=True
)

print("\n--- Train Sample ---")
sample_sid = next(iter(train_session_data.keys()))
print(
    f"Session {sample_sid}: AIDs {train_session_data[sample_sid]['aids'][:5]}..., User Group {train_session_data[sample_sid]['user_group']}")
print(f"Total train sessions: {len(train_session_data)}")

# %% [Step 2] Vocabulary + Time split (FIXED ORDER)

# --- 1. 先做时间排序切分 ---
all_sessions = list(train_session_data.keys())
all_timestamps = [train_session_data[sid]['ts'][-1] for sid in all_sessions]
sorted_sessions = [x for _, x in sorted(zip(all_timestamps, all_sessions))]
split_idx = int(len(sorted_sessions) * 0.8)
train_keys = sorted_sessions[:split_idx]
val_keys = sorted_sessions[split_idx:]

train_data_subset = {k: train_session_data[k] for k in train_keys}
val_data_subset = {k: train_session_data[k] for k in val_keys}
train_ground_truth_subset = {k: train_ground_truth[k] for k in train_keys if k in train_ground_truth}
val_ground_truth_subset = {k: train_ground_truth[k] for k in val_keys if k in train_ground_truth}

if 'val_sample_n_sessions' in CONFIG and CONFIG['val_sample_n_sessions'] is not None:
    val_sample_size = min(CONFIG['val_sample_n_sessions'], len(val_data_subset))
    import random

    random.seed(42)
    sampled_val_keys = random.sample(list(val_data_subset.keys()), val_sample_size)
    val_data_subset = {k: val_data_subset[k] for k in sampled_val_keys}
    val_ground_truth_subset = {k: val_ground_truth_subset[k] for k in sampled_val_keys if k in val_ground_truth_subset}
    print(f"✅ Validation set sampled: {len(val_data_subset)} sessions (from {len(val_keys)})")

# --- 2. 构建完整词汇表 ---
all_aids = set()

# 从 session events 中收集
for d in list(train_session_data.values()) + list(test_session_data.values()):
    all_aids.update(d['aids'])

# ✅ 从 ground truth 中收集所有商品（确保 eval 不漏）
print("✅ Collecting AIDs from train_ground_truth...")
for sid, gt in train_ground_truth.items():
    for action_type in ['clicks', 'carts', 'orders']:
        all_aids.update(gt[action_type])

print(f"✅ Final unique aids collected: {len(all_aids)}")

# 创建映射
aid_to_idx = {aid: idx + 1 for idx, aid in enumerate(all_aids)}
idx_to_aid = {idx + 1: aid for idx, aid in enumerate(all_aids)}
vocab_size = len(aid_to_idx) + 1  # +1 for padding (index 0)
print(f"✅ Vocabulary size (incl. padding): {vocab_size}")

# ✅ 验证映射一致性
print("=== Validating Mapping ===")
for aid in list(train_session_data.values())[0]['aids'][:10]:
    if aid not in aid_to_idx:
        print(f"❗ Aid {aid} not in vocabulary!")
        break
else:
    print("✅ All aids in vocabulary.")


# %% [Step 2b] OttoDataset with type and timestamp

class OttoDataset(Dataset):
    def __init__(self, session_data, ground_truth, aid_to_idx, max_len=30, is_test=False):
        self.session_ids = list(session_data.keys())
        self.session_data = session_data
        self.ground_truth = ground_truth
        self.aid_to_idx = aid_to_idx
        self.max_len = max_len
        self.is_test = is_test

    def __len__(self):
        return len(self.session_ids)

    def __getitem__(self, idx):
        session_id = self.session_ids[idx]
        data = self.session_data[session_id]
        aids = data['aids']
        types = data['types']
        tss = data['ts']

        if not isinstance(aids, list) or not isinstance(types, list) or not isinstance(tss, list):
            pad_tensor = lambda: torch.zeros(self.max_len, dtype=torch.long)
            user_tensor = torch.tensor(0, dtype=torch.long)
            if self.is_test:
                return pad_tensor(), pad_tensor(), pad_tensor(), user_tensor, int(session_id)
            else:
                return pad_tensor(), pad_tensor(), pad_tensor(), user_tensor, {
                    'clicks': [],
                    'carts': [],
                    'orders': []
                }

        aid_indices = [self.aid_to_idx.get(a, 0) for a in aids]
        type_indices = types
        ts_values = tss

        if len(aid_indices) < self.max_len:
            pad_len = self.max_len - len(aid_indices)
            aid_indices = [0] * pad_len + aid_indices
            type_indices = [0] * pad_len + type_indices
            ts_values = [0] * pad_len + ts_values
        else:
            aid_indices = aid_indices[-self.max_len:]
            type_indices = type_indices[-self.max_len:]
            ts_values = ts_values[-self.max_len:]

        user_group = int(data['user_group'])
        aid_tensor = torch.tensor(aid_indices, dtype=torch.long)
        type_tensor = torch.tensor(type_indices, dtype=torch.long)
        ts_tensor = torch.tensor(ts_values, dtype=torch.long)
        user_tensor = torch.tensor(user_group, dtype=torch.long)

        if self.is_test:
            return aid_tensor, type_tensor, ts_tensor, user_tensor, int(session_id)
        else:
            gt = self.ground_truth.get(session_id, {
                'clicks': [],
                'carts': [],
                'orders': []
            })
            gt_idx = {}
            for k, v in gt.items():
                gt_idx[k] = []
                if isinstance(v, list):
                    for a in v:
                        if a in self.aid_to_idx:
                            idx_val = self.aid_to_idx[a]
                            if idx_val > 0:
                                gt_idx[k].append(idx_val)
            return aid_tensor, type_tensor, ts_tensor, user_tensor, gt_idx


# 重新构建数据集
train_dataset = OttoDataset(train_data_subset, train_ground_truth_subset, aid_to_idx, max_len=CONFIG['max_seq_len'],
    is_test=False)
val_dataset = OttoDataset(val_data_subset, val_ground_truth_subset, aid_to_idx, max_len=CONFIG['max_seq_len'],
    is_test=False)
test_dataset = OttoDataset(test_session_data, {}, aid_to_idx, max_len=CONFIG['max_seq_len'], is_test=True)

print(f"✅ Train/Val split: {len(train_dataset)} train, {len(val_dataset)} val")

# ✅ 验证数据集
print("=== Validating Dataset ===")
for i in range(min(5, len(train_dataset))):
    try:
        sample = train_dataset[i]
        assert sample is not None, f"Sample {i} is None"
        assert len(sample) == 5, f"Sample {i} has {len(sample)} elements, expected 5"
        print(f"Sample {i}: OK")
    except Exception as e:
        print(f"❌ Error in sample {i}: {e}")
        raise
print("✅ Dataset validation passed!")


# %% [Step 3] Advanced Model with CoDA-MoE + Dropless + SwiGLU + RMSNorm

class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-8):
        super().__init__()
        self.scale = dim ** -0.5
        self.eps = eps
        self.g = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        norm = torch.norm(x, dim=-1, keepdim=True) * self.scale
        return x / (norm + self.eps) * self.g


class SwiGLU(nn.Module):
    def forward(self, x):
        x, gate = x.chunk(2, dim=-1)
        return x * F.silu(gate)


class TransformerEncoderLayerEnhanced(nn.Module):
    def __init__(self, d_model, nhead, dim_feedforward=2048, dropout=0.1, layer_norm_eps=1e-5):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.linear1 = nn.Linear(d_model, dim_feedforward * 2)
        self.activation = SwiGLU()
        self.dropout1 = nn.Dropout(dropout)
        self.linear2 = nn.Linear(dim_feedforward, d_model)
        self.dropout2 = nn.Dropout(dropout)
        self.norm1 = RMSNorm(d_model, eps=layer_norm_eps)
        self.norm2 = RMSNorm(d_model, eps=layer_norm_eps)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src, src_mask=None, src_key_padding_mask=None, is_causal=False):
        src2 = self.self_attn(src, src, src, attn_mask=src_mask, key_padding_mask=src_key_padding_mask)[0]
        src = src + self.dropout(src2)
        src = self.norm1(src)
        src2 = self.linear2(self.dropout1(self.activation(self.linear1(src))))
        src = src + self.dropout2(src2)
        src = self.norm2(src)
        return src


class TaskBasedMoE_CoDA_Dropless(nn.Module):
    def __init__(self, num_experts, input_dim, task_emb_dim, expert_hidden_dim=256, dropout=0.1, max_capacity=64,
                 coda_lambda=0.1):
        super().__init__()
        self.num_experts = num_experts
        self.max_capacity = max_capacity
        self.coda_lambda = coda_lambda
        self.task_embedding = nn.Embedding(3, task_emb_dim)

        self.task_router = nn.Sequential(
            nn.Linear(task_emb_dim + input_dim, input_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(input_dim, num_experts),
            nn.Sigmoid()
        )

        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(input_dim, expert_hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(expert_hidden_dim, input_dim),
            ) for _ in range(num_experts)
        ])

        self.expert_scorers = nn.ModuleList([nn.Linear(input_dim, 1) for _ in range(num_experts)])
        self.layer_norm = nn.LayerNorm(input_dim)

    def compute_coda_loss(self, expert_outputs, selected_indices_list):
        if len(expert_outputs) == 0:
            return torch.tensor(0.0, device='cpu')
        losses = []
        for i in range(len(expert_outputs)):
            if expert_outputs[i].size(0) == 0:
                continue
            mean_out_i = expert_outputs[i].mean(dim=0, keepdim=True)
            for j in range(i + 1, len(expert_outputs)):
                if expert_outputs[j].size(0) == 0:
                    continue
                mean_out_j = expert_outputs[j].mean(dim=0, keepdim=True)
                sim = F.cosine_similarity(mean_out_i, mean_out_j).mean()
                losses.append(1.0 - sim)  # 鼓励差异
        return torch.mean(torch.stack(losses)) if losses else torch.tensor(0.0, device=expert_outputs[0].device)

    def forward(self, x, task_ids, session_emb, return_coda_loss=False):
        B, D = x.shape
        task_emb = self.task_embedding(task_ids)
        router_input = torch.cat([task_emb, session_emb], dim=1)
        task_weights = self.task_router(router_input)

        final_output = torch.zeros_like(x)
        expert_outputs = []
        selected_indices_list = []

        capacity_factor = 1.5
        dynamic_capacity = int(capacity_factor * B / self.num_experts)
        topk_per_expert = min(dynamic_capacity, self.max_capacity)

        for eid in range(self.num_experts):
            scores = self.expert_scorers[eid](session_emb).squeeze(1)
            mask = (task_weights[:, eid] >= 0.5).float()
            masked_scores = scores * mask + (-1e9) * (1 - mask)

            if B <= topk_per_expert:
                topk_indices = torch.arange(B, device=x.device)
            else:
                _, topk_indices = torch.topk(masked_scores, topk_per_expert, dim=0)

            if len(topk_indices) == 0:
                expert_outputs.append(torch.zeros(0, D, device=x.device))
                selected_indices_list.append(torch.zeros(0, dtype=torch.long, device=x.device))
                continue

            selected_x = x[topk_indices]
            expert_out = self.experts[eid](selected_x)
            weights = torch.softmax(scores[topk_indices], dim=0).unsqueeze(1)
            task_w = task_weights[topk_indices, eid].unsqueeze(1)
            combined_weights = weights * task_w
            final_output.index_add_(0, topk_indices, combined_weights * expert_out)
            expert_outputs.append(expert_out)
            selected_indices_list.append(topk_indices)

        final_output = self.layer_norm(final_output + x)
        coda_loss = self.compute_coda_loss(expert_outputs, selected_indices_list) if return_coda_loss else None

        if self.training and torch.rand(1).item() < 0.01:
            loads = [len(idx) for idx in selected_indices_list]
            print(f"Expert loads: {loads}, Dynamic capacity: {topk_per_expert}")

        if return_coda_loss:
            return final_output, coda_loss
        else:
            return final_output


class OttoTransformerEnhanced(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, num_heads=4, num_layers=2, num_experts=3, max_len=30):
        super().__init__()
        self.embed_dim = embed_dim
        self.max_len = max_len
        self.aid_embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.type_embedding = nn.Embedding(3, embed_dim)
        self.pos_embedding = nn.Embedding(max_len, embed_dim)
        self.time_embedding = nn.Embedding(1441, embed_dim)

        encoder_layer = TransformerEncoderLayerEnhanced(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=embed_dim * 4,
            dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.moe = TaskBasedMoE_CoDA_Dropless(
            num_experts=num_experts,
            input_dim=embed_dim,
            task_emb_dim=16,
            expert_hidden_dim=256,
            dropout=0.1,
            max_capacity=CONFIG['max_capacity'],
            coda_lambda=CONFIG['coda_lambda']
        )

        self.output_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, aid_seq, type_seq, ts_seq, user_group):
        B, L = aid_seq.shape
        x = self.aid_embedding(aid_seq)
        x = x + self.type_embedding(type_seq)

        if L > 1:
            ts_diff = torch.diff(ts_seq.float(), dim=1)
            ts_diff_minutes = (ts_diff / 60000).clamp(0, 1440).long()
            ts_diff_emb = self.time_embedding(ts_diff_minutes)
            zero_pad = torch.zeros(B, 1, self.embed_dim, device=x.device)
            ts_diff_emb = torch.cat([zero_pad, ts_diff_emb], dim=1)
        else:
            ts_diff_emb = torch.zeros(B, L, self.embed_dim, device=x.device)

        x = x + ts_diff_emb
        pos = torch.arange(L, device=aid_seq.device).unsqueeze(0).expand(B, -1)
        x = x + self.pos_embedding(pos)

        padding_mask = (aid_seq == 0)
        x = self.transformer(x, src_key_padding_mask=padding_mask)
        x_last = x[:, -1, :]

        x_out, coda_loss = self.moe(x_last, user_group, x_last, return_coda_loss=True)
        x_out = self.output_proj(x_out)
        x_out = F.normalize(x_out, p=2, dim=1)

        return x_out, coda_loss, x  # 返回 seq 表示用于 next-item loss


device = torch.device(CONFIG['device'])
print("device", device)

model = OttoTransformerEnhanced(
    vocab_size=vocab_size,
    embed_dim=CONFIG['embed_dim'],
    num_experts=CONFIG['num_experts'],
    num_layers=CONFIG['num_layers'],
    max_len=CONFIG['max_seq_len']
).to(device)

# ✅ 初始化 embedding
with torch.no_grad():
    model.aid_embedding.weight.normal_(0, 0.02)
    model.aid_embedding.weight[0] = 0  # padding
print("✅ aid_embedding reinitialized.")
print("AID emb norm:", model.aid_embedding.weight.norm(dim=1).mean().item())

print("✅ Model created with CoDA + Dropless MoE + Next-Item Contrastive Loss.")

# %% [Step 4] DataLoader
train_loader = DataLoader(
    train_dataset,
    batch_size=CONFIG['batch_size'],
    shuffle=True,
    num_workers=CONFIG['num_workers'],
    pin_memory=True,
    collate_fn=collate_train,
    persistent_workers=(CONFIG['num_workers'] > 0)
)

val_loader = DataLoader(
    val_dataset,
    batch_size=CONFIG['batch_size'],
    shuffle=False,
    num_workers=CONFIG['num_workers'],
    pin_memory=True,
    collate_fn=collate_train,
    persistent_workers=(CONFIG['num_workers'] > 0)
)

test_loader = DataLoader(
    test_dataset,
    batch_size=CONFIG['batch_size'],
    shuffle=False,
    num_workers=CONFIG['num_workers'],
    pin_memory=True,
    collate_fn=collate_test,
    persistent_workers=(CONFIG['num_workers'] > 0)
)


# %% [Step 4b] Training with Multi-Objective Loss

def session_level_infonce_loss(session_emb, gts, aid_to_idx, aid_embeddings, temperature=0.05, device='cuda',
                               max_negatives=100):
    losses = []
    B = session_emb.size(0)
    all_aids = torch.arange(1, aid_embeddings.size(0), device=device)

    for i in range(B):
        anchor = session_emb[i]
        pos_indices = set()
        for typ in ['clicks', 'carts', 'orders']:
            for aid in gts[i].get(typ, []):
                if aid in aid_to_idx:
                    idx = aid_to_idx[aid]
                    if 0 < idx < aid_embeddings.size(0):
                        pos_indices.add(idx)
        if len(pos_indices) == 0:
            continue

        pos_indices = list(pos_indices)
        pos_embs = aid_embeddings[pos_indices]
        neg_mask = ~torch.isin(all_aids, torch.tensor(pos_indices, device=device))
        neg_candidates = all_aids[neg_mask]

        if len(neg_candidates) == 0:
            continue

        if len(neg_candidates) > max_negatives:
            perm = torch.randperm(len(neg_candidates), device=device)[:max_negatives]
            neg_indices = neg_candidates[perm]
        else:
            neg_indices = neg_candidates

        neg_embs = aid_embeddings[neg_indices]
        candidates = torch.cat([pos_embs, neg_embs], dim=0)
        logits = torch.matmul(anchor, candidates.T) / temperature
        log_prob = F.log_softmax(logits, dim=0)
        positive_log_probs = log_prob[:len(pos_embs)]
        loss = -positive_log_probs.mean()
        losses.append(loss)

    return torch.stack(losses).mean() if losses else torch.tensor(0.0, device=device)


def next_item_contrastive_loss_vectorized(seq_embs, aid_seq, padding_mask, temperature=0.1, device='cuda',
                                          max_negatives=100):
    B, L, D = seq_embs.shape
    valid_mask = ~(padding_mask[:, :-1] | padding_mask[:, 1:])
    if not valid_mask.any():
        return torch.tensor(0.0, device=device)

    batch_idx, time_idx = torch.where(valid_mask)
    anchors = seq_embs[batch_idx, time_idx]
    pos_aid_indices = aid_seq[batch_idx, time_idx + 1]
    pos_embs = model.aid_embedding.weight[pos_aid_indices]

    all_non_padding_mask = ~padding_mask
    all_aid_indices = aid_seq[all_non_padding_mask]
    all_candidate_embs = model.aid_embedding.weight[all_aid_indices]

    total_loss = 0.0
    count = 0
    for i in range(len(anchors)):
        anchor = anchors[i]
        pos_emb = pos_embs[i].unsqueeze(0)
        neg_mask = all_aid_indices != pos_aid_indices[i].item()
        neg_candidates = all_candidate_embs[neg_mask]
        if len(neg_candidates) == 0:
            continue
        if len(neg_candidates) > max_negatives:
            perm = torch.randperm(len(neg_candidates), device=device)[:max_negatives]
            neg_embs = neg_candidates[perm]
        else:
            neg_embs = neg_candidates
        candidates = torch.cat([pos_emb, neg_embs], dim=0)
        logits = torch.matmul(anchor, candidates.T) / temperature
        labels = torch.zeros(len(logits), device=device, dtype=torch.long)
        labels[0] = 1
        total_loss += F.cross_entropy(logits.unsqueeze(0), labels[:1])
        count += 1

    return total_loss / count if count > 0 else torch.tensor(0.0, device=device)


def train_multi_objective_enhanced(model, train_loader, device, epochs=3):
    optimizer = torch.optim.AdamW(model.parameters(), lr=CONFIG['learning_rate'], weight_decay=CONFIG['weight_decay'])
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=int(total_steps * CONFIG['warmup_ratio']), num_training_steps=total_steps
    )
    scaler = torch.amp.GradScaler('cuda') if device.type == 'cuda' else None

    for epoch in range(epochs):
        model.train()
        total_infonce = 0.0
        total_next = 0.0
        total_coda = 0.0
        cnt_batches = 0
        pbar = tqdm(train_loader, desc=f"Epoch {epoch + 1}/{epochs}")

        for batch_idx, (aid_seq, type_seq, ts_seq, user_group, gts) in enumerate(pbar):
            aid_seq = aid_seq.to(device, non_blocking=True)
            type_seq = type_seq.to(device, non_blocking=True)
            ts_seq = ts_seq.to(device, non_blocking=True)
            user_group = user_group.to(device, non_blocking=True)
            optimizer.zero_grad()

            with torch.amp.autocast(device_type=device.type):
                session_emb, coda_loss, seq_embs = model(aid_seq, type_seq, ts_seq, user_group)
                session_emb = F.normalize(session_emb, p=2, dim=1)
                aid_embeddings = F.normalize(model.aid_embedding.weight, p=2, dim=1)

                infonce_loss = session_level_infonce_loss(session_emb, gts, aid_to_idx, aid_embeddings,
                    temperature=CONFIG['temperature'], device=device)
                next_loss = next_item_contrastive_loss_vectorized(seq_embs, aid_seq, padding_mask=(aid_seq == 0),
                    temperature=CONFIG['temperature'], device=device)

                total_batch_loss = infonce_loss + 0.5 * next_loss + CONFIG['coda_lambda'] * coda_loss

            if scaler:
                scaler.scale(total_batch_loss).backward()
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), CONFIG['grad_clip'])
                scaler.step(optimizer)
                scaler.update()
            else:
                total_batch_loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), CONFIG['grad_clip'])
                optimizer.step()

            scheduler.step()
            total_infonce += infonce_loss.item()
            total_next += next_loss.item()
            total_coda += coda_loss.item()
            cnt_batches += 1

            if batch_idx == 0 and epoch == 0:
                print("\n=== DEBUG: After First Batch ===")
                print(
                    f"Infonce Loss: {infonce_loss.item():.4f}, Next Loss: {next_loss.item():.4f}, CoDA Loss: {coda_loss.item():.4f}")

            pbar.set_postfix({
                'InfoNCE': f"{infonce_loss.item():.4f}",
                'Next': f"{next_loss.item():.4f}",
                'CoDA': f"{coda_loss.item():.4f}"
            })

        avg_infonce = total_infonce / cnt_batches if cnt_batches else 0
        avg_next = total_next / cnt_batches if cnt_batches else 0
        avg_coda = total_coda / cnt_batches if cnt_batches else 0
        print(
            f"Epoch {epoch + 1} done. Avg InfoNCE: {avg_infonce:.6f}, Avg Next: {avg_next:.6f}, Avg CoDA: {avg_coda:.6f}")


# ✅ 开始训练
print("=== Debug: Checking first batch ===")
for batch in train_loader:
    print("GT sample:", batch[4][0])
    print("AID range in batch:", batch[0].min().item(), "to", batch[0].max().item())
    break

train_multi_objective_enhanced(model, train_loader, device, epochs=CONFIG['epochs'])


# %% [Step 5] Evaluation & Submission (略，保持不变)
# %% [Step 5] Enhanced Evaluation with Configurable Sample Size

def evaluate_enhanced_metrics(model, data_loader, aid_to_idx, idx_to_aid, device, top_k_list=[20, 50]):
    """
    Enhanced evaluation with configurable sample size and debugging.
    """
    print("\n=== Debug: Are all session embeddings the same? ===")
    first_batch = next(iter(val_loader))
    aid_seq, type_seq, ts_seq, user_group, _ = first_batch
    aid_seq = aid_seq.to(device)
    type_seq = type_seq.to(device)
    ts_seq = ts_seq.to(device)
    user_group = user_group.to(device)

    model.eval()
    with torch.no_grad():
        session_embs, _, _ = model(aid_seq, type_seq, ts_seq, user_group)
        session_embs = F.normalize(session_embs, p=2, dim=1)

    # 计算两两之间的 cosine similarity
    sim_matrix = torch.matmul(session_embs, session_embs.T)
    print("Similarity matrix (first 5x5):")
    print(sim_matrix[:5, :5].cpu().numpy())

    mean_sim = sim_matrix.triu(diagonal=1).mean().item()
    print(f"Average pairwise similarity: {mean_sim:.4f}")

    # ✅ 检查第一个 batch 的 GT aids 是否在词表中
    print("=== Validating: Are GT AIDs in vocabulary? ===")
    first_batch_gts = None
    for batch in val_loader:
        if len(batch) == 5:
            _, _, _, _, gts = batch
            first_batch_gts = gts
            break

    if first_batch_gts is not None:
        check_count = 0
        missing_count = 0
        for gt in first_batch_gts:
            for typ in ['clicks', 'carts', 'orders']:
                for aid in gt.get(typ, []):
                    check_count += 1
                    if aid not in aid_to_idx:
                        missing_count += 1
        if missing_count == 0:
            print(f"✅ All {check_count} GT aids in vocab.")
        else:
            print(f"❗ {missing_count}/{check_count} GT aids NOT in vocab!")

    model.eval()
    # 使用完整 embedding 表（含 padding）
    aid_embeddings = F.normalize(model.aid_embedding.weight, p=2, dim=1).to(device)

    metrics = {
        'recall@20': {
            'clicks': [],
            'carts': [],
            'orders': []
        },
        'hitrate@50': {
            'clicks': [],
            'carts': [],
            'orders': []
        },
        'mrr@20': {
            'clicks': [],
            'carts': [],
            'orders': []
        }
    }

    # 控制评估数量
    max_eval_batches = (CONFIG['eval_sample_n_sessions'] + CONFIG['batch_size'] - 1) // CONFIG['batch_size']
    print(f"Evaluating on up to {CONFIG['eval_sample_n_sessions']} sessions ({max_eval_batches} batches)...")

    with torch.no_grad():
        batch_count = 0
        for batch_idx, batch in enumerate(tqdm(data_loader, desc="Evaluating", total=max_eval_batches)):
            if batch_idx >= max_eval_batches:
                break

            sess_emb = None
            if len(batch) == 5:
                aid_seq, type_seq, ts_seq, user_group, gts = batch
                aid_seq = aid_seq.to(device, non_blocking=True)
                type_seq = type_seq.to(device, non_blocking=True)
                ts_seq = ts_seq.to(device, non_blocking=True)
                user_group = user_group.to(device, non_blocking=True)
                sess_emb, _, _ = model(aid_seq, type_seq, ts_seq, user_group)
            else:
                aid_seq, type_seq, ts_seq, user_group, session_ids = batch
                aid_seq = aid_seq.to(device, non_blocking=True)
                type_seq = type_seq.to(device, non_blocking=True)
                ts_seq = ts_seq.to(device, non_blocking=True)
                user_group = user_group.to(device, non_blocking=True)
                sess_emb, _, _ = model(aid_seq, type_seq, ts_seq, user_group)
                gts = [{} for _ in range(len(session_ids))]

            # 归一化 session embeddings
            sess_emb = F.normalize(sess_emb, p=2, dim=1)
            scores = torch.matmul(sess_emb, aid_embeddings.T)

            max_k = max(top_k_list)
            k = min(max_k, scores.shape[1])
            _, topk_idx = torch.topk(scores, k=k, dim=1)

            for i in range(topk_idx.shape[0]):
                preds = []
                for idx in topk_idx[i]:
                    aid_idx = idx.item()
                    if aid_idx == 0:
                        continue
                    if aid_idx in idx_to_aid:
                        preds.append(idx_to_aid[aid_idx])
                    if len(preds) >= max_k:
                        break
                pred_list = preds[:max_k]
                pred_set = set(pred_list)
                gt = gts[i]

                for typ in ['clicks', 'carts', 'orders']:
                    true_idx_list = gt.get(typ, [])
                    if len(true_idx_list) == 0:
                        continue
                    true_aids = set()
                    for ii in true_idx_list:
                        if ii in idx_to_aid:
                            true_aids.add(idx_to_aid[ii])
                    if len(true_aids) == 0:
                        continue

                    # Recall@20
                    denom_20 = min(20, len(true_aids))
                    hits_20 = len(set(pred_list[:20]) & true_aids)
                    metrics['recall@20'][typ].append(hits_20 / denom_20)

                    # HitRate@50
                    hits_50 = len(set(pred_list[:50]) & true_aids)
                    metrics['hitrate@50'][typ].append(1.0 if hits_50 > 0 else 0.0)

                    # MRR@20
                    mrr_score = 0.0
                    for rank, pred_aid in enumerate(pred_list[:20], 1):
                        if pred_aid in true_aids:
                            mrr_score = 1.0 / rank
                            break
                    metrics['mrr@20'][typ].append(mrr_score)

            batch_count += 1

    # 计算平均指标
    avg_metrics = {}
    for metric_name, metric_dict in metrics.items():
        avg_metrics[metric_name] = {}
        for typ in metric_dict:
            avg_metrics[metric_name][typ] = np.mean(metric_dict[typ]) if len(metric_dict[typ]) > 0 else 0.0

    # 加权得分
    weighted_recall_20 = (
            0.10 * avg_metrics['recall@20']['clicks'] +
            0.30 * avg_metrics['recall@20']['carts'] +
            0.60 * avg_metrics['recall@20']['orders']
    )
    weighted_hitrate_50 = (
            0.10 * avg_metrics['hitrate@50']['clicks'] +
            0.30 * avg_metrics['hitrate@50']['carts'] +
            0.60 * avg_metrics['hitrate@50']['orders']
    )
    weighted_mrr_20 = (
            0.10 * avg_metrics['mrr@20']['clicks'] +
            0.30 * avg_metrics['mrr@20']['carts'] +
            0.60 * avg_metrics['mrr@20']['orders']
    )

    print(f"\n📊 Enhanced Metrics:")
    for metric_name in avg_metrics:
        print(f"{metric_name}: clicks {avg_metrics[metric_name]['clicks']:.4f}, "
              f"carts {avg_metrics[metric_name]['carts']:.4f}, "
              f"orders {avg_metrics[metric_name]['orders']:.4f}")
    print(f"🏆 Weighted Recall@20: {weighted_recall_20:.4f}")
    print(f"🏆 Weighted HitRate@50: {weighted_hitrate_50:.4f}")
    print(f"🏆 Weighted MRR@20: {weighted_mrr_20:.4f}")

    return avg_metrics, weighted_recall_20


# --- 开始评估 ---
print("\n--- Evaluating on Validation Set with Enhanced Metrics ---")
print("=== Debug: Checking first val batch ===")
for batch in val_loader:
    if len(batch) == 5:
        aid_seq, type_seq, ts_seq, user_group, gts = batch
        print("Val GT sample:", gts[0])
        break

# 运行评估
val_metrics, val_score = evaluate_enhanced_metrics(
    model, val_loader, aid_to_idx, idx_to_aid, device,
    top_k_list=CONFIG['top_k_list']
)

