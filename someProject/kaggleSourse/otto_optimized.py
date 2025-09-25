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
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

# 配置参数
DATA_DIR = '/kaggle/input/otto-recommender-system'
TRAIN_PATH = f'{DATA_DIR}/train.jsonl'
TEST_PATH = f'{DATA_DIR}/test.jsonl'
MAX_TRAIN_SESS = 2_000_000
TOP_K_POP = 200
WEIGHTS = {'clicks': 1, 'carts': 3, 'orders': 5}

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
BATCH_SIZE = 128
EPOCHS = 3
MAX_SEQ_LEN = 200
CANDIDATE_K = 150
NUM_ITEMS = 1_856_630

# Cell 2: 优化版召回策略
class OptimizedRecallGenerator:
    def __init__(self, train_path, max_sess=2_000_000, cache_dir='./cache'):
        self.train_path = train_path
        self.max_sess = max_sess
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # 参数优化
        self.MAX_RECENT_ITEMS = 15
        self.TOP_K_POPULAR = 150
        self.CANDIDATE_POOL_SIZE = 200
        self.BEHAVIOR_WEIGHTS = {'clicks': 1, 'carts': 3, 'orders': 5}
        self.TOP_K_FREQ_ITEMS_FOR_CF = 20_000  # 增加高频商品数量
        self.CF_SIM_TOPK = 50
        
        self.global_pop = Counter()
        self.item_sim = {}
        self.top_pop = []
        self._build_pop_and_cf()

    def _build_pop_and_cf(self):
        cache_file = f"{self.cache_dir}/recall_cache.pkl"
        
        # 尝试加载缓存
        if os.path.exists(cache_file):
            print("📦 加载召回缓存...")
            with open(cache_file, 'rb') as f:
                cache_data = pickle.load(f)
                self.global_pop = cache_data['global_pop']
                self.item_sim = cache_data['item_sim']
                self.top_pop = cache_data['top_pop']
            print(f"✅ 缓存加载完成: 全局热度商品数: {len(self.global_pop)}, Item-CF覆盖: {len(self.item_sim)}")
            return
            
        print("正在构建召回策略（优化版）...")
        
        # 第一步：统计全局热度
        with open(self.train_path, 'r') as f:
            for idx, line in enumerate(tqdm(f, total=self.max_sess, desc="📊 统计全局热度"), 1):
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
        
        # 第三步：构建Item-CF（使用更高效的数据结构）
        cf_builder = OptimizedTopKDict(k=self.CF_SIM_TOPK)
        
        with open(self.train_path, 'r') as f:
            for idx, line in enumerate(tqdm(f, total=self.max_sess, desc="🔄 构建Item-CF"), 1):
                if idx > self.max_sess:
                    break
                events = orjson.loads(line)['events']
                
                # 优化：只考虑最近的交互，并增加权重
                seen = {}
                session_aids = []
                for i, e in enumerate(reversed(events)):
                    aid = e['aid']
                    weight = self.BEHAVIOR_WEIGHTS[e['type']]
                    if aid in top_freq_aids:
                        if aid not in seen:
                            seen[aid] = weight
                            session_aids.append((aid, weight))
                        else:
                            seen[aid] = max(seen[aid], weight)  # 取最大权重
                        if len(session_aids) >= 50:
                            break
                
                session_aids.reverse()
                
                # 构建加权共现对
                n = len(session_aids)
                for i in range(n):
                    for j in range(i + 1, n):
                        aid1, w1 = session_aids[i]
                        aid2, w2 = session_aids[j]
                        cooccur_weight = w1 * w2  # 权重相乘
                        cf_builder.update_pair(aid1, aid2, cooccur_weight)
        
        self.item_sim = cf_builder.finalize(k_final=self.CF_SIM_TOPK)
        
        # 保存缓存
        cache_data = {
            'global_pop': self.global_pop,
            'item_sim': self.item_sim,
            'top_pop': self.top_pop
        }
        with open(cache_file, 'wb') as f:
            pickle.dump(cache_data, f)
        
        print(f"[构建完成] 全局热度商品数: {len(self.global_pop)}, Item-CF覆盖商品数: {len(self.item_sim)}")

    def get_candidates(self, events, top_k=None):
        top_k = top_k or self.CANDIDATE_POOL_SIZE
        
        # 1. Recency: 最近交互的不重复商品（考虑权重）
        last_n = []
        seen = set()
        for e in reversed(events):
            aid = e['aid']
            if aid not in seen:
                last_n.append((aid, self.BEHAVIOR_WEIGHTS[e['type']]))
                seen.add(aid)
                if len(last_n) >= self.MAX_RECENT_ITEMS:
                    break
        
        # 2. Item-CF扩展（考虑权重）
        cf_candidates = {}
        for aid, weight in last_n:
            if aid in self.item_sim:
                for sim_aid in self.item_sim[aid]:
                    if sim_aid not in cf_candidates:
                        cf_candidates[sim_aid] = weight
                    else:
                        cf_candidates[sim_aid] = max(cf_candidates[sim_aid], weight)
        
        # 3. 按权重排序并添加热门商品
        sorted_candidates = sorted(cf_candidates.items(), key=lambda x: x[1], reverse=True)
        candidates = [aid for aid, _ in sorted_candidates[:top_k]]
        
        # 4. 补充热门商品
        for aid in self.top_pop:
            if len(candidates) >= top_k:
                break
            if aid not in candidates:
                candidates.append(aid)
        
        return candidates[:top_k]

class OptimizedTopKDict:
    """优化的Top-K字典，支持权重"""
    def __init__(self, k=50):
        self.k = k
        self.data = defaultdict(list)

    def update_pair(self, aid1, aid2, weight):
        """更新加权共现关系"""
        # 使用更高效的更新策略
        self._update_item(aid1, aid2, weight)
        self._update_item(aid2, aid1, weight)

    def _update_item(self, aid, sim_aid, weight):
        heap = self.data[aid]
        # 检查是否已存在
        for i, (w, sid) in enumerate(heap):
            if sid == sim_aid:
                heap[i] = (max(w, weight), sid)  # 更新权重
                return
        
        # 添加新的相似商品
        if len(heap) < self.k:
            heap.append((weight, sim_aid))
        else:
            # 找到最小权重
            min_idx = min(range(len(heap)), key=lambda i: heap[i][0])
            if weight > heap[min_idx][0]:
                heap[min_idx] = (weight, sim_aid)

    def finalize(self, k_final=50):
        result = {}
        for aid, heap in self.data.items():
            sorted_sims = sorted(heap, key=lambda x: (-x[0], x[1]))
            result[aid] = [aid for _, aid in sorted_sims[:k_final]]
        return result

# Cell 3: 改进的模型架构
class ImprovedSparseAttention(nn.Module):
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.out_proj = nn.Linear(embed_dim, embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        B, L, D = x.shape
        H, E = self.num_heads, self.head_dim
        
        q = self.q_proj(x).view(B, L, H, E).transpose(1, 2)
        k = self.k_proj(x).view(B, L, H, E).transpose(1, 2)
        v = self.v_proj(x).view(B, L, H, E).transpose(1, 2)
        
        attn = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(E)
        
        if mask is not None:
            attn = attn.masked_fill(mask == 0, -1e9)
        
        attn = torch.softmax(attn, dim=-1)
        attn = self.dropout(attn)
        
        out = torch.matmul(attn, v).transpose(1, 2).contiguous().view(B, L, D)
        return self.out_proj(out)

class ImprovedLightSANSLayer(nn.Module):
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        self.self_attn = ImprovedSparseAttention(embed_dim, num_heads, dropout)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(embed_dim * 4, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x, mask=None):
        # 残差连接 + 层归一化
        x = self.norm1(x + self.self_attn(x, mask))
        x = self.norm2(x + self.ffn(x))
        return x

class ImprovedTimeAwareLightSANs(nn.Module):
    def __init__(self, num_items, embed_dim=128, num_heads=4, num_layers=2, 
                 max_seq_len=200, dropout=0.1):
        super().__init__()
        self.embed_dim = embed_dim
        self.item_emb = nn.Embedding(num_items + 1, embed_dim, padding_idx=0)
        self.type_emb = nn.Embedding(3, embed_dim // 4)
        self.type_proj = nn.Linear(embed_dim // 4, embed_dim)
        self.time_emb = nn.Linear(1, embed_dim)
        self.pos_emb = nn.Embedding(max_seq_len, embed_dim)
        self.dropout = nn.Dropout(dropout)
        
        self.layers = nn.ModuleList([
            ImprovedLightSANSLayer(embed_dim, num_heads, dropout) 
            for _ in range(num_layers)
        ])
        
        # 添加最终投影层
        self.final_proj = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

    def forward(self, item_seq, type_seq, time_delta_seq, candidate_ids, mask=None):
        B, L = item_seq.shape
        device = item_seq.device
        
        # 商品嵌入
        x = self.item_emb(item_seq)
        
        # 类型嵌入
        type_e = self.type_emb(type_seq)
        type_e = self.type_proj(type_e)
        x += type_e
        
        # 时间嵌入
        x += self.time_emb(time_delta_seq.unsqueeze(-1))
        
        # 位置嵌入
        x += self.pos_emb(torch.arange(L, device=device))
        x = self.dropout(x)
        
        # 通过Transformer层
        for layer in self.layers:
            x = layer(x, mask)
        
        # 最终投影
        x = self.final_proj(x)
        
        # 获取会话表示
        session_rep = x[:, -1, :]  # [B, D]
        candidate_emb = self.item_emb(torch.clamp(candidate_ids, min=0))  # [B, K, D]
        logits = torch.bmm(candidate_emb, session_rep.unsqueeze(-1)).squeeze(-1)  # [B, K]
        
        # 掩码填充位置
        valid_mask = (candidate_ids != -1)
        logits = logits.masked_fill(~valid_mask, -1e9)
        
        return logits

class ImprovedMoELightSANs(nn.Module):
    def __init__(self, num_items, embed_dim=128, num_experts=3, dropout=0.1):
        super().__init__()
        self.experts = nn.ModuleList([
            ImprovedTimeAwareLightSANs(num_items, embed_dim, dropout=dropout) 
            for _ in range(num_experts)
        ])
        
        # 改进的门控网络
        self.gate = nn.Sequential(
            nn.Linear(4, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(16, num_experts)
        )
        
        # 添加温度参数
        self.temperature = nn.Parameter(torch.ones(1))

    def forward(self, item_seq, type_seq, time_delta_seq, candidate_ids, session_stats, mask=None):
        gate_logits = self.gate(session_stats) / self.temperature
        gate_weights = torch.softmax(gate_logits, dim=-1)
        
        outputs = []
        for expert in self.experts:
            logits = expert(item_seq, type_seq, time_delta_seq, candidate_ids, mask)
            outputs.append(logits.unsqueeze(-1))
        
        outputs = torch.cat(outputs, dim=-1)
        return (outputs * gate_weights.unsqueeze(1)).sum(-1)

# Cell 4: 优化的数据集和训练
def compute_session_stats(events):
    """计算会话统计特征（改进版）"""
    n = len(events)
    if n == 0:
        return torch.tensor([0.0, 0.0, 0.0, 0.0], dtype=torch.float32)
    
    types = [e['type'] for e in events]
    click_ratio = types.count('clicks') / n
    cart_ratio = types.count('carts') / n
    order_ratio = types.count('orders') / n
    
    # 添加会话长度特征
    return torch.tensor([n, click_ratio, cart_ratio, order_ratio], dtype=torch.float32)

def prepare_seq_features(events, max_len=MAX_SEQ_LEN):
    """准备序列特征（修复时间差计算）"""
    aids = [e['aid'] for e in events]
    type_map = {'clicks': 0, 'carts': 1, 'orders': 2}
    types = [type_map[e['type']] for e in events]
    ts = [e['ts'] for e in events]
    
    # 修复时间差计算
    time_delta = [0.0]
    for i in range(1, len(ts)):
        delta = (ts[i] - ts[i-1]) / 1000.0  # 转换为秒
        time_delta.append(min(delta, 3600.0))  # 限制最大时间差为1小时
    
    # 截断到最大长度
    aids = aids[-max_len:]
    types = types[-max_len:]
    time_delta = time_delta[-max_len:]
    
    # 填充
    pad_len = max_len - len(aids)
    aids = [0] * pad_len + aids
    types = [0] * pad_len + types
    time_delta = [0.0] * pad_len + time_delta
    
    return (torch.tensor(aids, dtype=torch.long),
            torch.tensor(types, dtype=torch.long),
            torch.tensor(time_delta, dtype=torch.float32))

class OptimizedOTTODataset(Dataset):
    """优化的数据集类，减少内存使用"""
    def __init__(self, jsonl_path, recall_gen, max_sess=MAX_TRAIN_SESS):
        self.jsonl_path = jsonl_path
        self.recall_gen = recall_gen
        self.max_sess = max_sess
        self.sessions_raw = []
        
        # 只存储文件偏移量，不存储原始数据
        self.file_offsets = []
        with open(jsonl_path, 'rb') as f:
            offset = 0
            for i, line in enumerate(f):
                if i >= max_sess:
                    break
                self.file_offsets.append(offset)
                offset += len(line)

    def __len__(self):
        return len(self.file_offsets)
    
    def __getitem__(self, idx):
        # 按需读取数据
        with open(self.jsonl_path, 'rb') as f:
            f.seek(self.file_offsets[idx])
            line = f.readline()
            sess = orjson.loads(line)
            events = sess['events']
        
        # 召回候选
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
    
    item_seq = torch.stack(item_seq)
    type_seq = torch.stack(type_seq)
    time_delta = torch.stack(time_delta)
    session_stats = torch.stack(session_stats)
    
    # 处理变长的candidates和labels
    max_k = CANDIDATE_K
    batch_size = len(candidates)
    
    candidates_padded = torch.full((batch_size, max_k), -1, dtype=torch.long)
    labels_padded = torch.zeros((batch_size, max_k), dtype=torch.float32)
    
    for i, (cand, lab) in enumerate(zip(candidates, labels)):
        k = len(cand)
        candidates_padded[i, :k] = cand
        labels_padded[i, :k] = lab
    
    return item_seq, type_seq, time_delta, candidates_padded, session_stats, labels_padded

# Cell 5: 改进的训练循环
class FocalLoss(nn.Module):
    """Focal Loss for handling class imbalance"""
    def __init__(self, alpha=1, gamma=2):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        
    def forward(self, inputs, targets):
        bce_loss = nn.functional.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        pt = torch.exp(-bce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * bce_loss
        return focal_loss.mean()

def train_model():
    print("🚀 开始构建召回器...")
    recall_gen = OptimizedRecallGenerator(TRAIN_PATH, max_sess=MAX_TRAIN_SESS)
    print(f"✅ Top pop: {recall_gen.top_pop[:5]}")
    print(f"✅ Item-CF covers {len(recall_gen.item_sim)} items")

    print("📚 加载数据集...")
    full_dataset = OptimizedOTTODataset(TRAIN_PATH, recall_gen, max_sess=MAX_TRAIN_SESS)
    train_size = int(0.9 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, val_size], 
        generator=torch.Generator().manual_seed(42)
    )

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, 
                             collate_fn=collate_fn, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, 
                           collate_fn=collate_fn, num_workers=2)

    print("🧠 初始化模型...")
    model = ImprovedMoELightSANs(num_items=NUM_ITEMS, embed_dim=128, num_experts=3).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion = FocalLoss(alpha=1, gamma=2)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)
    
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
            
            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            train_loss += loss.item()
        
        scheduler.step()
        
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
            true_set = set(torch.where(all_labels[i] == 1)[0].tolist())
            pred_set = set(top20_pred[i].tolist())
            if len(true_set) > 0:
                recall_at_20 += len(true_set & pred_set) / len(true_set)
        recall_at_20 /= all_labels.size(0)
        
        print(f"Epoch {epoch+1}: Loss={train_loss/len(train_loader):.4f}, Recall@20={recall_at_20:.4f}, LR={scheduler.get_last_lr()[0]:.6f}")
        
        if recall_at_20 > best_val_recall:
            best_val_recall = recall_at_20
            torch.save(model.state_dict(), "best_model_optimized.pth")
            print("✅ 保存最佳模型")

    print(f"🎯 最佳验证 Recall@20: {best_val_recall:.4f}")
    return model, recall_gen

# Cell 6: 改进的预测和提交
def generate_submission(model, recall_gen):
    print("🔍 生成提交文件...")
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
    submission_df.to_csv('submission_optimized.csv', index=False)
    print(f"✅ 提交文件已保存！共 {len(output_rows)} 行。")

if __name__ == "__main__":
    model, recall_gen = train_model()
    generate_submission(model, recall_gen)
