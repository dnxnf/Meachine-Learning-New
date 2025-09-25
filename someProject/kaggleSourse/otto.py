# Cell 1: 配置与导入
import os
import json
import time
import orjson
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict, Counter
import pandas as pd
from tqdm import tqdm
import math

# 配置参数（与你最初一致）
DATA_DIR       = '/kaggle/input/otto-recommender-system'
TRAIN_PATH     = f'{DATA_DIR}/train.jsonl'
TEST_PATH      = f'{DATA_DIR}/test.jsonl'
MAX_TRAIN_SESS = 2_000_000
TOP_K_POP      = 200
WEIGHTS        = {'clicks':1, 'carts':3, 'orders':5}

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
BATCH_SIZE = 128
EPOCHS = 3
MAX_SEQ_LEN = 200
CANDIDATE_K = 150
NUM_ITEMS = 1_856_630  # OTTO aid 范围
# recall_strategies.py（内存优化版：Pop + Recency + 轻量 Item-CF）
import orjson
from collections import Counter, defaultdict
from heapq import heappush, heappop

class RecallGenerator:
    # ========== 可调参数 ==========
    MAX_RECENT_ITEMS = 10          # 从 15 → 10（减少候选）
    TOP_K_POPULAR = 100
    CANDIDATE_POOL_SIZE = 150      # 从 200 → 150
    BEHAVIOR_WEIGHTS = {'clicks': 1, 'carts': 3, 'orders': 5}
    TOP_K_FREQ_ITEMS_FOR_CF = 10_000  # 从 30k → 10k（关键！）
    CF_SIM_TOPK = 30               # 从 50 → 30

    def __init__(self, train_path, max_sess=2_000_000):
        self.train_path = train_path
        self.max_sess = max_sess
        self.global_pop = Counter()
        self.item_sim = {}
        self.top_pop = []
        self._build_pop_and_cf()

    def _build_pop_and_cf(self):
        print("正在统计全局热度与轻量 Item-CF（内存优化版）...")
        
        # 第一步：统计全局热度（带进度条）
        with open(self.train_path, 'r') as f:
            for idx, line in enumerate(tqdm(f, total=self.max_sess, desc="📊 统计全局热度", mininterval=1.0), 1):
                session = orjson.loads(line)
                for event in session['events']:
                    weight = self.BEHAVIOR_WEIGHTS[event['type']]
                    self.global_pop[event['aid']] += weight
                if idx >= self.max_sess:
                    break
    
        # 第二步：确定高频商品集合
        top_freq_aids = set(
            aid for aid, _ in self.global_pop.most_common(self.TOP_K_FREQ_ITEMS_FOR_CF)
        )
        self.top_pop = [aid for aid, _ in self.global_pop.most_common(self.TOP_K_POPULAR)]
    
        # 第三步：构建轻量 Item-CF（带进度条！）
        cf_builder = TopKDict(k=self.CF_SIM_TOPK)
        
        with open(self.train_path, 'r') as f:
            for idx, line in enumerate(tqdm(f, total=self.max_sess, desc="🔄 构建 Item-CF", mininterval=1.0), 1):
                if idx > self.max_sess:
                    break
                events = orjson.loads(line)['events']
                
                # 提取高频且去重的 aids（最多取最后 50 个）
                seen = set()
                session_aids = []
                for e in reversed(events):
                    aid = e['aid']
                    if aid in top_freq_aids and aid not in seen:
                        session_aids.append(aid)
                        seen.add(aid)
                        if len(session_aids) >= 50:
                            break
                session_aids.reverse()
    
                # 构建共现对
                n = len(session_aids)
                for i in range(n):
                    for j in range(i + 1, n):
                        cf_builder.update_pair(session_aids[i], session_aids[j])

    # 第四步：提取最终相似列表
        self.item_sim = cf_builder.finalize(k_final=self.CF_SIM_TOPK)
    
        print(f"[构建完成] 全局热度商品数: {len(self.global_pop)}, "
              f"Item-CF 覆盖商品数: {len(self.item_sim)}")

    def get_candidates(self, events, top_k=None):
        top_k = top_k or self.CANDIDATE_POOL_SIZE
        
        # 1. Recency: 最近交互的不重复商品
        last_n = []
        for e in reversed(events):
            if e['aid'] not in last_n:
                last_n.append(e['aid'])
                if len(last_n) >= self.MAX_RECENT_ITEMS:
                    break

        # 2. Item-CF 扩展
        cf_candidates = set(last_n)
        for aid in last_n:
            if len(cf_candidates) >= top_k:
                break
            if aid in self.item_sim:
                for sim_aid in self.item_sim[aid]:
                    cf_candidates.add(sim_aid)
                    if len(cf_candidates) >= top_k:
                        break

        # 3. 补充热门商品
        candidates = list(cf_candidates)
        for aid in self.top_pop:
            if len(candidates) >= top_k:
                break
            if aid not in candidates:
                candidates.append(aid)
                
        return candidates[:top_k]

class TopKDict:
    """为每个 aid 动态维护共现最高的 Top-K 相似商品（使用最小堆）"""
    def __init__(self, k=50):
        self.k = k
        self.data = defaultdict(list)  # aid -> min-heap of (cooccur_count, sim_aid)

    def update_pair(self, aid1, aid2):
        """更新 aid1 与 aid2 的共现关系（对称）"""
        # aid1 -> aid2
        heap1 = self.data[aid1]
        if len(heap1) < self.k:
            heappush(heap1, (1, aid2))
        else:
            # 堆顶是最小值，若新共现 >= 堆顶，则替换
            if 1 > heap1[0][0] or (1 == heap1[0][0] and len(heap1) < self.k):
                heappop(heap1)
                heappush(heap1, (1, aid2))
            elif heap1[0][0] == 1:
                # 允许多个相同计数，但限制总数（可选）
                pass  # 简化：只记录是否共现，不累加多次（见下文说明）

        # aid2 -> aid1
        heap2 = self.data[aid2]
        if len(heap2) < self.k:
            heappush(heap2, (1, aid1))
        else:
            if 1 > heap2[0][0] or (1 == heap2[0][0] and len(heap2) < self.k):
                heappop(heap2)
                heappush(heap2, (1, aid1))

    def finalize(self, k_final=50):
        """最终提取每个 aid 的 Top-K 相似商品（按共现强度降序）"""
        result = {}
        for aid, heap in self.data.items():
            # 堆中是 (count, sim_aid)，按 count 降序排序
            sorted_sims = sorted(heap, key=lambda x: (-x[0], x[1]))
            result[aid] = [aid for _, aid in sorted_sims[:k_final]]
        return result


# Cell 3: MoE-LightSANs 模型
class SparseAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.out_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        B, L, D = x.shape
        H, E = self.num_heads, self.head_dim
        q = self.q_proj(x).view(B, L, H, E).transpose(1, 2)
        k = self.k_proj(x).view(B, L, H, E).transpose(1, 2)
        v = self.v_proj(x).view(B, L, H, E).transpose(1, 2)
        attn = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(E)
        attn = torch.softmax(attn, dim=-1)
        out = torch.matmul(attn, v).transpose(1, 2).contiguous().view(B, L, D)
        return self.out_proj(out)

class LightSANSLayer(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.self_attn = SparseAttention(embed_dim, num_heads)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 2),
            nn.ReLU(),
            nn.Linear(embed_dim * 2, embed_dim)
        )
        self.norm2 = nn.LayerNorm(embed_dim)

    def forward(self, x):
        x = self.norm1(x + self.self_attn(x))
        x = self.norm2(x + self.ffn(x))
        return x

class TimeAwareLightSANs(nn.Module):
    def __init__(self, num_items, embed_dim=128, num_heads=4, num_layers=2, max_seq_len=200):
        super().__init__()
        self.embed_dim = embed_dim
        self.item_emb = nn.Embedding(num_items + 1, embed_dim, padding_idx=0)
        self.type_emb = nn.Embedding(3, 16)  # 原始 type embedding
        self.type_proj = nn.Linear(16, embed_dim)  # 投影到 embed_dim
        self.time_emb = nn.Linear(1, embed_dim)
        self.pos_emb = nn.Embedding(max_seq_len, embed_dim)
        self.layers = nn.ModuleList([
            LightSANSLayer(embed_dim, num_heads) for _ in range(num_layers)
        ])

    def forward(self, item_seq, type_seq, time_delta_seq, candidate_ids):
        B, L = item_seq.shape
        device = item_seq.device
        
        x = self.item_emb(item_seq)  # [B, L, D]
        
        # Type embedding: [B, L] → [B, L, 16] → [B, L, D]
        type_e = self.type_emb(type_seq)  # [B, L, 16]
        type_e = self.type_proj(type_e)   # [B, L, D]
        x += type_e
        
        # Time embedding
        x += self.time_emb(time_delta_seq.unsqueeze(-1))  # [B, L, 1] → [B, L, D]
        
        # Position embedding
        x += self.pos_emb(torch.arange(L, device=device))  # [L, D] → broadcast to [B, L, D]
        
        for layer in self.layers:
            x = layer(x)
        
        session_rep = x[:, -1, :]  # [B, D]
        candidate_emb = self.item_emb(torch.clamp(candidate_ids, min=0))  # [B, K, D]
        logits = torch.bmm(candidate_emb, session_rep.unsqueeze(-1)).squeeze(-1)  # [B, K]
        
        # Mask padding positions (candidate_ids == -1)
        valid_mask = (candidate_ids != -1)
        logits = logits.masked_fill(~valid_mask, -1e9)
        
        return logits

class MoELightSANs(nn.Module):
    def __init__(self, num_items, embed_dim=128, num_experts=2):
        super().__init__()
        self.experts = nn.ModuleList([
            TimeAwareLightSANs(num_items, embed_dim) for _ in range(num_experts)
        ])
        self.gate = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, num_experts)
        )

    def forward(self, item_seq, type_seq, time_delta_seq, candidate_ids, session_stats):
        gate_logits = self.gate(session_stats)
        gate_weights = torch.softmax(gate_logits, dim=-1)
        outputs = []
        for expert in self.experts:
            logits = expert(item_seq, type_seq, time_delta_seq, candidate_ids)
            outputs.append(logits.unsqueeze(-1))
        outputs = torch.cat(outputs, dim=-1)
        return (outputs * gate_weights.unsqueeze(1)).sum(-1)
    # Cell 4: 数据集 + 训练
def compute_session_stats(events):
    n = len(events)
    types = [e['type'] for e in events]
    click_ratio = types.count('clicks') / n
    cart_ratio = types.count('carts') / n
    order_ratio = types.count('orders') / n
    return torch.tensor([n, click_ratio, cart_ratio, order_ratio], dtype=torch.float32)

def prepare_seq_features(events, max_len=MAX_SEQ_LEN):
    aids = [e['aid'] for e in events]
    type_map = {'clicks': 0, 'carts': 1, 'orders': 2}
    types = [type_map[e['type']] for e in events]
    ts = [e['ts'] for e in events]
    time_delta = [0] + [(ts[i] - ts[i-1]) // 1000 for i in range(1, len(ts))]
    aids = aids[-max_len:]
    types = types[-max_len:]
    time_delta = time_delta[-max_len:]
    pad_len = max_len - len(aids)
    aids = [0] * pad_len + aids
    types = [0] * pad_len + types
    time_delta = [0] * pad_len + time_delta
    return (torch.tensor(aids, dtype=torch.long),
            torch.tensor(types, dtype=torch.long),
            torch.tensor(time_delta, dtype=torch.float32))

class OTTODataset(Dataset):
    def __init__(self, jsonl_path, recall_gen, max_sess=MAX_TRAIN_SESS):
        self.jsonl_path = jsonl_path
        self.recall_gen = recall_gen
        self.max_sess = max_sess
        # 只存储原始 session 字符串，不解析！
        self.sessions_raw = []
        with open(jsonl_path, 'rb') as f:
            for i, line in enumerate(f):
                if i >= max_sess:
                    break
                self.sessions_raw.append(line)

    def __len__(self):
        return len(self.sessions_raw)
    
    def __getitem__(self, idx):
        # 实时解析 + 生成特征（省内存！）
        line = self.sessions_raw[idx]
        sess = orjson.loads(line)
        events = sess['events']
        
        # 召回候选（固定长度 CANDIDATE_K）
        candidates = self.recall_gen.get_candidates(events, top_k=CANDIDATE_K)
        ordered_aids = {e['aid'] for e in events if e['type'] == 'orders'}
        labels = [1 if aid in ordered_aids else 0 for aid in candidates]
        
        # 构建序列特征
        item_seq, type_seq, time_delta = prepare_seq_features(events)
        session_stats = compute_session_stats(events)
        
        return (
            item_seq,
            type_seq,
            time_delta,
            torch.tensor(candidates, dtype=torch.long),
            session_stats,
            torch.tensor(labels, dtype=torch.float32)
        )

def collate_fn(batch):
    item_seq, type_seq, time_delta, candidates, session_stats, labels = zip(*batch)
    
    # 固定长度的直接 stack
    item_seq = torch.stack(item_seq)
    type_seq = torch.stack(type_seq)
    time_delta = torch.stack(time_delta)
    session_stats = torch.stack(session_stats)
    
    # 处理变长的 candidates 和 labels → padding to CANDIDATE_K
    max_k = CANDIDATE_K
    batch_size = len(candidates)
    
    # 初始化填充 tensor
    candidates_padded = torch.full((batch_size, max_k), -1, dtype=torch.long)  # -1 表示 padding
    labels_padded = torch.zeros((batch_size, max_k), dtype=torch.float32)
    
    for i, (cand, lab) in enumerate(zip(candidates, labels)):
        k = len(cand)
        candidates_padded[i, :k] = cand
        labels_padded[i, :k] = lab
    
    return item_seq, type_seq, time_delta, candidates_padded, session_stats, labels_padded

# 开始训练
print("🚀 开始构建召回器...")
recall_gen = RecallGenerator(TRAIN_PATH, max_sess=MAX_TRAIN_SESS)
print(f"✅ Top pop: {recall_gen.top_pop[:5]}")
print(f"✅ Item-CF covers {len(recall_gen.item_sim)} items")


print("📚 加载数据集...")
full_dataset = OTTODataset(TRAIN_PATH, recall_gen, max_sess=MAX_TRAIN_SESS)
train_size = int(0.9 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size], generator=torch.Generator().manual_seed(42))

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)

print("🧠 初始化模型...")
model = MoELightSANs(num_items=NUM_ITEMS, embed_dim=128, num_experts=2).to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.BCEWithLogitsLoss()
best_val_recall = 0.0


for epoch in range(EPOCHS):
    model.train()
    train_loss = 0.0
    for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}"):
        item_seq, type_seq, time_delta, candidates, session_stats, labels = [x.to(DEVICE) for x in batch]
        optimizer.zero_grad()
        logits = model(item_seq, type_seq, time_delta, candidates, session_stats)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    
    # 验证
    model.eval()
    all_labels, all_preds = [], []
    with torch.no_grad():
        for batch in val_loader:
            item_seq, type_seq, time_delta, candidates, session_stats, labels = [x.to(DEVICE) for x in batch]
            logits = model(item_seq, type_seq, time_delta, candidates, session_stats)
            probs = torch.sigmoid(logits)
            all_labels.append(labels.cpu())
            all_preds.append(probs.cpu())
    
    all_labels = torch.cat(all_labels, dim=0)
    all_preds = torch.cat(all_preds, dim=0)
    top20_pred = torch.topk(all_preds, 20, dim=1).indices
    recall_at_20 = 0.0
    for i in range(all_labels.size(0)):
        # # 注意：这是候选池内的 Recall@20，用于评估排序模型
        true_set = set(torch.where(all_labels[i] == 1)[0].tolist())
        pred_set = set(top20_pred[i].tolist())
        if len(true_set) > 0:
            recall_at_20 += len(true_set & pred_set) / len(true_set)
    recall_at_20 /= all_labels.size(0)
    
    print(f"Epoch {epoch+1}: Loss={train_loss/len(train_loader):.4f}, Recall@20={recall_at_20:.4f}")
    if recall_at_20 > best_val_recall:
        best_val_recall = recall_at_20
        torch.save(model.state_dict(), "best_model.pth")
        print("✅ 保存最佳模型")

print(f"🎯 最佳验证 Recall@20: {best_val_recall:.4f}")
# Cell 5: 生成提交文件
print("🔍 加载最佳模型进行预测...")
model = MoELightSANs(num_items=NUM_ITEMS, embed_dim=128, num_experts=2).to(DEVICE)
model.load_state_dict(torch.load("best_model.pth", map_location=DEVICE))
model.eval()

output_rows = []
with open(TEST_PATH, 'rb') as f:
    for line in tqdm(f, desc="预测测试集"):
        sess = orjson.loads(line)
        events = sess['events']
        session_id = sess['session']
        candidates = recall_gen.get_candidates(events, top_k=CANDIDATE_K)
        item_seq, type_seq, time_delta = prepare_seq_features(events)
        session_stats = compute_session_stats(events)
        
        with torch.no_grad():
            logits = model(
                item_seq.unsqueeze(0).to(DEVICE),
                type_seq.unsqueeze(0).to(DEVICE),
                time_delta.unsqueeze(0).to(DEVICE),
                torch.tensor(candidates, dtype=torch.long).unsqueeze(0).to(DEVICE),
                session_stats.unsqueeze(0).to(DEVICE)
            )
            probs = torch.sigmoid(logits[0]).cpu()
        
        top10_idx = torch.topk(probs, 10).indices
        top10_aids = [candidates[i] for i in top10_idx]
        top10_str = ' '.join(map(str, top10_aids))
        
        for typ in ['clicks', 'carts', 'orders']:
            output_rows.append({'session_type': f'{session_id}_{typ}', 'labels': top10_str})

submission_df = pd.DataFrame(output_rows)
submission_df.to_csv('submission.csv', index=False)
print(f"✅ 提交文件已保存！共 {len(output_rows)} 行。")