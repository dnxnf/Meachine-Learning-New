#%% md
# # Dependencies
#%%
# install colmap(CPU)
!cd /kaggle/input/pkg-colmap/colmap_offline && dpkg -i ./*.deb

# test
!colmap -h
#%%
# IMPORTANT 
#Install dependencies and copy model weights to run the notebook without internet access when submitting to the competition.

!pip install --no-index /kaggle/input/imc2024-packages-lightglue-rerun-kornia/* --no-deps
!mkdir -p /root/.cache/torch/hub/checkpoints
!cp /kaggle/input/aliked/pytorch/aliked-n16/1/aliked-n16.pth /root/.cache/torch/hub/checkpoints/
!cp /kaggle/input/aliked/pytorch/aliked-n32/1/aliked-n32.pth /root/.cache/torch/hub/checkpoints/
!cp /kaggle/input/aliked/pytorch/aliked-n16rot/1/aliked-n16rot.pth /root/.cache/torch/hub/checkpoints/
!cp /kaggle/input/lightglue/pytorch/aliked/1/aliked_lightglue.pth /root/.cache/torch/hub/checkpoints/
!cp /kaggle/input/lightglue/pytorch/aliked/1/aliked_lightglue.pth /root/.cache/torch/hub/checkpoints/aliked_lightglue_v0-1_arxiv-pth
#%%
import sys
import os, glob
from tqdm import tqdm
from fastprogress import progress_bar
from time import time, sleep
import gc
import numpy as np
import h5py
import dataclasses
import pandas as pd
from IPython.display import clear_output
from collections import defaultdict
from copy import deepcopy
from PIL import Image
import networkx as nx

import cv2
import torch
import torch.nn.functional as F
import kornia as K
import kornia.feature as KF

import torch
from lightglue import match_pair
from lightglue import ALIKED, LightGlue
from lightglue.utils import load_image, rbd
from transformers import AutoImageProcessor, AutoModel

# IMPORTANT Utilities: importing data into colmap and competition metric
import pycolmap
sys.path.append('/kaggle/input/imc25-utils')
from database import *
from h5_to_db import *
import metric
# Do not forget to select an accelerator on the sidebar to the right.
#device = K.utils.get_cuda_device_if_available(0)
#print(f'{device=}')

import concurrent.futures
#%% md
# # Configurations
#%%
class Param_AlikedLightGlue:
    def __init__(
        self,
        min_matches = 15,
        max_num_keypoints = 4096,
        image_size = 1024,
    ):
        self.min_matches = min_matches
        self.max_num_keypoints = max_num_keypoints
        self.image_size = image_size
        
class CONFIG:
    # Image pairs
    sim_th = 2.0
    min_pairs = 20
    exhaustive_if_less = 20
    GLOBAL_TOPK    = 150 # 50 # 近傍候補数
    N_KEYPOINTS    = 2048          # 1画像あたり上限
    RATIO_THR      = 1.0               # Lowe ratio
    MATCH_THRESH   = 15                # good?matches 閾値

    # Image Matching
    params_alikedlg = [
        #Param_AlikedLightGlue( min_matches = 15, max_num_keypoints = 4096, image_size = 512 ),
        #Param_AlikedLightGlue( min_matches = 15, max_num_keypoints = 4096, image_size = 1024 ),
        #Param_AlikedLightGlue( min_matches = 15, max_num_keypoints = 8192, image_size = 1536 ),
        Param_AlikedLightGlue( min_matches = 50, max_num_keypoints = 8192, image_size = 1536 ),
        #Param_AlikedLightGlue( min_matches = 50, max_num_keypoints = 4096*3, image_size = 1536 ),
    ]

    roma_max_num_keypoints = 512
    roma_image_size = 140
    roma_batch_size = 20

    # SfM
    num_pallalel_sfm = 4
#%%
device0=torch.device('cuda:0')
device1=torch.device('cuda:1')

def switch_gpu(device, device_index):
    if device is None:
        return device0, 0
    elif device == device0:
        return device1, 1
    else:
        return device0, 0
#%% md
# # Colmap Utilities
#%%
def import_into_colmap(img_dir, feature_dir ='.featureout', database_path = 'colmap.db'):
    db = COLMAPDatabase.connect(database_path)
    db.create_tables()
    single_camera = False
    fname_to_id = add_keypoints(db, feature_dir, img_dir, '', 'simple-radial', single_camera)
    add_matches(
        db,
        feature_dir,
        fname_to_id,
    )
    db.commit()
    return
#%%
def add_keypoints_with_scene(db, scene, h5_path, image_path, img_ext, camera_model, single_camera = True):
    keypoint_f = h5py.File(os.path.join(h5_path, 'keypoints.h5'), 'r')

    camera_id = None
    fname_to_id = {}
    for filename in tqdm(list(keypoint_f.keys())):
        if not filename in scene:
            continue
        
        keypoints = keypoint_f[filename][()]

        fname_with_ext = filename# + img_ext
        path = os.path.join(image_path, fname_with_ext)
        if not os.path.isfile(path):
            raise IOError(f'Invalid image path {path}')

        if camera_id is None or not single_camera:
            camera_id = create_camera(db, path, camera_model)
        image_id = db.add_image(fname_with_ext, camera_id)
        fname_to_id[filename] = image_id

        db.add_keypoints(image_id, keypoints)

    return fname_to_id

def add_matches_with_scene(db, scene, h5_path, fname_to_id):
    match_file = h5py.File(os.path.join(h5_path, 'matches.h5'), 'r')
    
    added = set()
    n_keys = len(match_file.keys())
    n_total = (n_keys * (n_keys - 1)) // 2

    with tqdm(total=n_total) as pbar:
        for key_1 in match_file.keys():
            if not key_1 in scene:
                continue

            group = match_file[key_1]
            for key_2 in group.keys():
                if not key_2 in scene:
                    continue
                    
                id_1 = fname_to_id[key_1]
                id_2 = fname_to_id[key_2]

                pair_id = image_ids_to_pair_id(id_1, id_2)
                if pair_id in added:
                    warnings.warn(f'Pair {pair_id} ({id_1}, {id_2}) already added!')
                    continue
            
                matches = group[key_2][()]
                db.add_matches(id_1, id_2, matches)

                added.add(pair_id)

                pbar.update(1)

def import_into_colmap_with_scene(img_dir, scene, feature_dir ='.featureout', database_path = 'colmap.db'):
    db = COLMAPDatabase.connect(database_path)
    db.create_tables()
    single_camera = False
    fname_to_id = add_keypoints(db, feature_dir, img_dir, '', 'simple-radial', single_camera)
    #fname_to_id = add_keypoints_with_scene(db, scene, feature_dir, img_dir, '', 'simple-radial', single_camera)
    add_matches_with_scene(
        db,
        scene,
        feature_dir,
        fname_to_id,
    )
    db.commit()
    return
#%% md
# # Pairs Reranker
#%%
import os, torch, urllib.request, tempfile
from PIL import Image
from tqdm import tqdm
from torchvision import transforms


# ---------- Global embeddings ---------- #
def _extract_dino_embeddings(fnames, device = torch.device('cuda')):
    processor = AutoImageProcessor.from_pretrained('/kaggle/input/dinov2/pytorch/base/1')
    model = AutoModel.from_pretrained('/kaggle/input/dinov2/pytorch/base/1')
    model = model.eval()
    model = model.to(device)
    global_descs_dinov2 = []
    for i, img_fname_full in tqdm(enumerate(fnames),total= len(fnames)):
        key = os.path.splitext(os.path.basename(img_fname_full))[0]
        timg = load_torch_image(img_fname_full)
        with torch.inference_mode():
            inputs = processor(images=timg, return_tensors="pt", do_rescale=False).to(device)
            outputs = model(**inputs)
            dino_mac = F.normalize(outputs.last_hidden_state[:,1:].max(dim=1)[0], dim=1, p=2)
        global_descs_dinov2.append(dino_mac.detach().cpu())
    global_descs_dinov2 = torch.cat(global_descs_dinov2, dim=0)
    return global_descs_dinov2

def _build_topk_lists(global_feats, device):
    """
    global_feats : (N, D)  L2?normed
    returns      : list of length?≤(N?1) neighbor indices for each image
    """
    g   = global_feats.to(device)          # (N,D)
    sim = g @ g.T                          # cosine similarity
    sim.fill_diagonal_(-1)

    N   = sim.size(0)
    k   = min(CONFIG.GLOBAL_TOPK, N - 1)   # ★ ここが修正点
    k   = max(k, 1)                        # 万一 N==2 でも k=1 を確保

    topk = torch.topk(sim, k, dim=1).indices.cpu()
    return [row.tolist() for row in topk]


# ---------- ALIKED local features ---------- #
def _get_aliked_model(device, num_features, resize_to=1024, detection_threshold=0.01):
    dtype = torch.float32 # ALIKED has issues with float16
    extractor = ALIKED(
        model_name="aliked-n16",
        max_num_keypoints=num_features,
        detection_threshold=detection_threshold, 
        resize=resize_to
    ).eval().to(device, dtype)
    extractor.preprocess_conf["resize"] = resize_to
    return extractor
    
@torch.no_grad()
def _extract_local_features(img_paths, model, device):
    dtype = torch.float32
    descs = []
    for p in tqdm(img_paths, desc="ALIKED"):
        image0 = load_torch_image(p, device=device).to(dtype)
        h, w = image0.shape[2], image0.shape[3]
        feats0 = model.extract(image0)  # auto-resize the image, disable with resize=None
        d = feats0['descriptors'].reshape(-1, 128).detach()
        descs.append(torch.nn.functional.normalize(d, dim=1).half().cpu())
    return descs


# ---------- good?match カウント (Torch) ---------- #
@torch.no_grad()
def _mutual_nn_score(desc1, desc2, device):
    if desc1.size(0) == 0 or desc2.size(0) == 0:
        return 0
    d12 = torch.cdist(desc1.to(device), desc2.to(device), p=2)
    min_val, _ = torch.min(d12, 1)
    n_matches = np.sum( min_val.cpu().numpy() < (CONFIG.RATIO_THR ** 2) )
    return n_matches

def _build_final_pairs(topk_lists, descs, device):
    pairs = []
    for i, nbrs in enumerate(tqdm(topk_lists, desc="Local verify")):
        for j in nbrs:
            if i < j:
                score = _mutual_nn_score(descs[i], descs[j], device)
                if score >= CONFIG.MATCH_THRESH:
                    pairs.append((i, j))
                    #pairs.append((i, j, score))
    pairs = sorted(list(set(pairs)))
    return pairs


# =========================================================
def get_image_pairs(fnames, device=torch.device("cuda")):
    """
    fnames: list[str] - 画像ファイルパスのリスト
    device: torch.device - 計算に使用する GPU / CPU
    returns: list[tuple[int,int]] - マッチングすべき画像 index ペア
    """
    assert len(fnames) > 1, "fnames must contain at least two images"

    # 1) DINO global features
    global_feats = _extract_dino_embeddings(fnames, device)
    topk_lists   = _build_topk_lists(global_feats, device)
    cnt = 0
    for topk_list in topk_lists:
        cnt += len(topk_list)
    print(cnt)

    # 2) ALIKED local descriptors
    aliked = _get_aliked_model(device, CONFIG.N_KEYPOINTS)
    descs  = _extract_local_features(fnames, aliked, device)

    # 3) local verification
    pairs  = _build_final_pairs(topk_lists, descs, device)

    del aliked
    torch.cuda.empty_cache()
    gc.collect()
    return pairs
# =========================================================
#%% md
# # Image pairs
#%%
def load_torch_image(fname, device=torch.device('cuda')):
    img = K.io.load_image(fname, K.io.ImageLoadType.RGB32, device=device)[None, ...]
    return img

# Must Use efficientnet global descriptor to get matching shortlists.
def get_global_desc(fnames, device = torch.device('cuda')):
    processor = AutoImageProcessor.from_pretrained('/kaggle/input/dinov2/pytorch/base/1')
    model = AutoModel.from_pretrained('/kaggle/input/dinov2/pytorch/base/1')
    model = model.eval()
    model = model.to(device)
    global_descs_dinov2 = []
    for i, img_fname_full in tqdm(enumerate(fnames),total= len(fnames)):
        key = os.path.splitext(os.path.basename(img_fname_full))[0]
        timg = load_torch_image(img_fname_full)
        with torch.inference_mode():
            inputs = processor(images=timg, return_tensors="pt", do_rescale=False).to(device)
            outputs = model(**inputs)
            dino_mac = F.normalize(outputs.last_hidden_state[:,1:].max(dim=1)[0], dim=1, p=2)
        global_descs_dinov2.append(dino_mac.detach().cpu())
    global_descs_dinov2 = torch.cat(global_descs_dinov2, dim=0)
    return global_descs_dinov2

def get_img_pairs_exhaustive(img_fnames):
    index_pairs = []
    for i in range(len(img_fnames)):
        for j in range(i+1, len(img_fnames)):
            index_pairs.append((i,j))
    return index_pairs

def get_image_pairs_shortlist(fnames,
                              sim_th = 0.6, # should be strict
                              min_pairs = 20,
                              exhaustive_if_less = 20,
                              device=torch.device('cuda')):
    num_imgs = len(fnames)
    if num_imgs <= exhaustive_if_less:
        return get_img_pairs_exhaustive(fnames)
    matching_list = get_image_pairs(fnames, device)
    return matching_list

#%% md
# # Aliked+LightGlue
#%%
def convert_coord(r, w, h, rotk):
    if rotk == 0:
        return r
    elif rotk == 1:
        rx = w-1-r[:, 1]
        ry = r[:, 0]
        return torch.concat([rx[None], ry[None]], dim=0).T # np.array([rx, ry]).T
    elif rotk == 2:
        rx = w-1-r[:, 0]
        ry = h-1-r[:, 1]
        return torch.concat([rx[None], ry[None]], dim=0).T # np.array([rx, ry]).T
    elif rotk == 3:
        rx = r[:, 1]
        ry = h-1-r[:, 0]
        return torch.concat([rx[None], ry[None]], dim=0).T # np.array([rx, ry]).T

def matching_aliked_lightglue_rot(
    img_fnames,
    index_pairs,
    rot,
    saved_file,
    feature_dir = '.featureout',
    num_features = 4096,
    resize_to = 1024,
    device=torch.device('cuda'),
    min_matches=15,
    verbose=True,
):
    if not os.path.isdir(feature_dir):
        os.makedirs(feature_dir)

    #####################################################
    # Extract keypoints and descriptions
    #####################################################
    dtype = torch.float32 # ALIKED has issues with float16
    extractor = ALIKED(
        model_name="aliked-n16",
        max_num_keypoints=num_features,
        detection_threshold=0.01, #0.001, 
        resize=resize_to
    ).eval().to(device, dtype)
    print("aliked> image size =", extractor.preprocess_conf["resize"], "-->", resize_to )
    extractor.preprocess_conf["resize"] = resize_to
    if not os.path.isdir(feature_dir):
        os.makedirs(feature_dir)
    
    dict_kpts_cuda = {}
    dict_descs_cuda = {}
    for img_path in img_fnames:
        img_fname = img_path.split('/')[-1]
        key = img_fname

        with torch.inference_mode():
            rot_k = 0
            image0 = load_torch_image(img_path, device=device).to(dtype)
            h, w = image0.shape[2], image0.shape[3]
            feats0 = extractor.extract(image0)  # auto-resize the image, disable with resize=None
            kpts = feats0['keypoints'].reshape(-1, 2).detach()
            descs = feats0['descriptors'].reshape(len(kpts), -1).detach()
            dict_kpts_cuda[f"{key}_{rot_k}"] = kpts
            dict_descs_cuda[f"{key}_{rot_k}"] = descs
            if verbose:
                print(f"aliked_rot> rot_k={rot_k}, kpts.shape={kpts.shape}, descs.shape={descs.shape}")

        if rot != 0:
            with torch.inference_mode():
                rot_k = rot
                image0 = load_torch_image(img_path, device=device).to(dtype)
                h, w = image0.shape[2], image0.shape[3]
                image1 = torch.rot90(image0, rot, [2, 3])
                feats0 = extractor.extract(image1)  # auto-resize the image, disable with resize=None
                kpts = feats0['keypoints'].reshape(-1, 2).detach()
                descs = feats0['descriptors'].reshape(len(kpts), -1).detach()
                kpts = convert_coord(kpts, w, h, rot_k)
                dict_kpts_cuda[f"{key}_{rot_k}"] = kpts
                dict_descs_cuda[f"{key}_{rot_k}"] = descs
                if verbose:
                    print(f"aliked_rot> rot_k={rot_k}, kpts.shape={kpts.shape}, descs.shape={descs.shape}")
    del extractor
    gc.collect()

    #####################################################
    # Matching keypoints
    #####################################################
    lg_matcher = KF.LightGlueMatcher(
        "aliked", {
            "width_confidence": -1,
            "depth_confidence": -1,
            #"filter_threshold": 0.5,
            "mp": True if 'cuda' in str(device) else False
        }
    ).eval().to(device).half()
    
    cnt_pairs = 0
    with h5py.File(saved_file, mode='w') as f_match:
        for pair_idx in tqdm(index_pairs):
            idx1, idx2 = pair_idx
            fname1, fname2 = img_fnames[idx1], img_fnames[idx2]
            if ("outliers" in fname1) or ( "outliers" in fname2 ):
                continue
            key1, key2 = fname1.split('/')[-1], fname2.split('/')[-1]
            
            kp1 = dict_kpts_cuda[f"{key1}_0"]
            desc1 = dict_descs_cuda[f"{key1}_0"]
                        
            kp2 = dict_kpts_cuda[f"{key2}_{rot}"]
            desc2 = dict_descs_cuda[f"{key2}_{rot}"]
            with torch.inference_mode():
                dists, idxs = lg_matcher(desc1.half(),
                                     desc2.half(),
                                     KF.laf_from_center_scale_ori(kp1.half()[None]),
                                     KF.laf_from_center_scale_ori(kp2.half()[None]))
            #print( f"dists.shape={dists.shape}")
            #print( f"type(dists)={type(dists)}")
            #print( f"dists.mean()={dists.mean()}, {dists.max()}, {dists.min()}")
            if len(idxs)  == 0:
                continue
            kp1 = kp1[idxs[:,0], :].cpu().numpy().reshape(-1, 2).astype(np.float32)
            kp2 = kp2[idxs[:,1], :].cpu().numpy().reshape(-1, 2).astype(np.float32)
            confs = (1.0-dists).cpu().numpy().reshape(-1, 1).astype(np.float32)
            n_matches = kp1.shape[0]
            group  = f_match.require_group(key1)
            if n_matches >= min_matches:
                matches = np.concatenate([kp1, kp2, confs], axis=1)
                #print(f"@@@@ matches.shape = {matches.shape}")
                group.create_dataset(key2, data=matches)
                cnt_pairs+=1
                if verbose:
                    print (f'aliked_rot> {key1}-{key2}@rot={rot}: {n_matches} matches @ {cnt_pairs}th pair')            
            else:
                if verbose:
                    print (f'aliked_rot> {key1}-{key2}: {n_matches} matches --> skipped')
    del lg_matcher
    torch.cuda.empty_cache()
    gc.collect()
    return


#%% md
# # Keypoints merger & Matching Filter
#%%
def get_unique_idxs(A, dim=0):
    # https://stackoverflow.com/questions/72001505/how-to-get-unique-elements-and-their-firstly-appeared-indices-of-a-pytorch-tenso
    unique, idx, counts = torch.unique(A, dim=dim, sorted=True, return_inverse=True, return_counts=True)
    _, ind_sorted = torch.sort(idx, stable=True)
    cum_sum = counts.cumsum(0)
    cum_sum = torch.cat((torch.tensor([0],device=cum_sum.device), cum_sum[:-1]))
    first_indices = ind_sorted[cum_sum]
    return first_indices

def get_keypoint_from_h5(fp, key1, key2):
    rc = -1
    try:
        kpts = np.array(fp[key1][key2])
        rc = 0
        return (rc, kpts)
    except:
        return (rc, None)

def get_keypoint_from_multi_h5(fps, key1, key2):
    list_mkpts = []
    for fp in fps:
        rc, mkpts = get_keypoint_from_h5(fp, key1, key2)
        if mkpts is not None:
            list_mkpts.append(mkpts)
    if len(list_mkpts) > 0:
        for data in list_mkpts:
            print(f"--> ", data.shape)
        list_mkpts = np.concatenate(list_mkpts, axis=0)
    else:
        list_mkpts = None
    return list_mkpts

def matches_merger(
    img_fnames,
    index_pairs,
    files_keypoints,
    save_file,
    feature_dir = 'featureout',
    filter_FundamentalMatrix = False,
    filter_iterations = 10,
    filter_threshold = 8,
    min_matches=15,
):
    print( files_keypoints )
    # open h5 files
    fps = [ h5py.File(file, mode="r") for file in files_keypoints ]
    
    with h5py.File(save_file, mode='w') as f_match:
        counter = 0
        for pair_idx in progress_bar(index_pairs):
            idx1, idx2 = pair_idx
            fname1, fname2 = img_fnames[idx1], img_fnames[idx2]
            key1, key2 = fname1.split('/')[-1], fname2.split('/')[-1]

            # extract keypoints
            mkpts = get_keypoint_from_multi_h5(fps, key1, key2)
            if mkpts is None:
                print(f"skipped key1={key1}, key2={key2}")
                continue

            ori_size = mkpts.shape[0]
            if mkpts.shape[0] < min_matches:
                continue
            
            if filter_FundamentalMatrix:
                store_inliers = { idx:0 for idx in range(mkpts.shape[0]) }
                idxs = np.array(range(mkpts.shape[0]))
                for iter in range(filter_iterations):
                    try:
                        Fm, inliers = cv2.findFundamentalMat(
                            mkpts[:,:2], mkpts[:,2:4], cv2.USAC_MAGSAC, 0.15, 0.9999, 20000)
                        if Fm is not None:
                            inliers = inliers > 0
                            inlier_idxs = idxs[inliers[:, 0]]
                            #print(inliers.shape, inlier_idxs[:5])
                            for idx in inlier_idxs:
                                store_inliers[idx] += 1
                    except:
                        print(f"Failed to cv2.findFundamentalMat. mkpts.shape={mkpts.shape}")
                inliers = np.array([ count for (idx, count) in store_inliers.items() ]) >= filter_threshold
                mkpts = mkpts[inliers]
                if mkpts.shape[0] < 15:
                    print(f"skipped key1={key1}, key2={key2}: mkpts.shape={mkpts.shape} after filtered.")
                    continue
                #print(f"filter_FundamentalMatrix: {len(store_inliers)} matches --> {mkpts.shape[0]} matches")
            
            
            print (f'{key1}-{key2}: {ori_size} --> {mkpts.shape[0]} matches')            
            # regist tmp file
            group  = f_match.require_group(key1)
            group.create_dataset(key2, data=mkpts[:, :4])
            counter += 1
    print( f"Ensembled pairs : {counter} pairs" )
    for fp in fps:
        fp.close()

def get_adjacent_edges_with_weights(G, node):
    """
    指定されたノードに隣接するエッジとその重みをリストで返す関数
    
    :param G: networkxのグラフオブジェクト
    :param node: 対象となるノード
    :return: (隣接ノード, 重み)のタプルのリスト、重みの降順でソートされる
    """
    adjacent_edges = [(neighbor, G[node][neighbor]['weight']) for neighbor in G.neighbors(node)]
    return sorted(adjacent_edges, key=lambda x: x[1], reverse=True)

def filter_mkpts(
    file_mkpts, 
    save_file,
    th_num_pairs,
):
    sleep(10)
    G = nx.Graph()
    pairs = []
    with h5py.File(save_file, mode='w') as f_match, h5py.File(file_mkpts, "r") as fp:
        for key1 in fp.keys():
            for key2 in fp[key1].keys():
                mkpts = fp[key1][key2]
                G.add_edge(key1, key2, weight=mkpts.shape[0])
                pairs.append([key1, key2, mkpts])

        for (key1, key2, mkpts) in pairs:
            neibors1 = get_adjacent_edges_with_weights(G, key1)
            neibors2 = get_adjacent_edges_with_weights(G, key2)
            if (key2 in [ val[0] for val in neibors1[:th_num_pairs] ]) or (key1 in [ val[0] for val in neibors2[:th_num_pairs] ]):
                group  = f_match.require_group(key1)
                group.create_dataset(key2, data=mkpts)

def keypoints_merger(
    img_fnames,
    index_pairs,
    files_keypoints,
    feature_dir = 'featureout',
    filter_FundamentalMatrix = False,
    filter_iterations = 10,
    filter_threshold = 8,
):
    print(f"files_keypoints = {files_keypoints}")
    save_file0 = f'{feature_dir}/merge_tmp0.h5'
    !rm -rf {save_file0}
    matches_merger(
        img_fnames,
        index_pairs,
        files_keypoints,
        save_file0,
        feature_dir = feature_dir,
        filter_FundamentalMatrix = filter_FundamentalMatrix,
        filter_iterations = filter_iterations,
        filter_threshold = filter_threshold,
    )

    th_num_pairs = 6
    save_file = f'{feature_dir}/merge_tmp.h5'
    !rm -rf {save_file}
    filter_mkpts(
        save_file0, 
        save_file,
        th_num_pairs,
    )
    
    # Let's find unique loftr pixels and group them together.
    kpts = defaultdict(list)
    match_indexes = defaultdict(dict)
    total_kpts=defaultdict(int)
    with h5py.File(save_file, mode='r') as f_match:
        for k1 in f_match.keys():
            group  = f_match[k1]
            for k2 in group.keys():
                matches = group[k2][...]
                total_kpts[k1]
                kpts[k1].append(matches[:, :2])
                kpts[k2].append(matches[:, 2:])
                current_match = torch.arange(len(matches)).reshape(-1, 1).repeat(1, 2)
                current_match[:, 0]+=total_kpts[k1]
                current_match[:, 1]+=total_kpts[k2]
                total_kpts[k1]+=len(matches)
                total_kpts[k2]+=len(matches)
                match_indexes[k1][k2]=current_match

    for k in kpts.keys():
        kpts[k] = np.round(np.concatenate(kpts[k], axis=0))
    unique_kpts = {}
    unique_match_idxs = {}
    out_match = defaultdict(dict)
    for k in kpts.keys():
        uniq_kps, uniq_reverse_idxs = torch.unique(torch.from_numpy(kpts[k]),dim=0, return_inverse=True)
        unique_match_idxs[k] = uniq_reverse_idxs
        unique_kpts[k] = uniq_kps.numpy()
    for k1, group in match_indexes.items():
        for k2, m in group.items():
            m2 = deepcopy(m)
            m2[:,0] = unique_match_idxs[k1][m2[:,0]]
            m2[:,1] = unique_match_idxs[k2][m2[:,1]]
            mkpts = np.concatenate([unique_kpts[k1][ m2[:,0]],
                                    unique_kpts[k2][  m2[:,1]],
                                   ],
                                   axis=1)
            unique_idxs_current = get_unique_idxs(torch.from_numpy(mkpts), dim=0)
            m2_semiclean = m2[unique_idxs_current]
            unique_idxs_current1 = get_unique_idxs(m2_semiclean[:, 0], dim=0)
            m2_semiclean = m2_semiclean[unique_idxs_current1]
            unique_idxs_current2 = get_unique_idxs(m2_semiclean[:, 1], dim=0)
            m2_semiclean2 = m2_semiclean[unique_idxs_current2]
            out_match[k1][k2] = m2_semiclean2.numpy()
    with h5py.File(f'{feature_dir}/keypoints.h5', mode='w') as f_kp:
        for k, kpts1 in unique_kpts.items():
            f_kp[k] = kpts1
    
    with h5py.File(f'{feature_dir}/matches.h5', mode='w') as f_match:
        for k1, gr in out_match.items():
            group  = f_match.require_group(k1)
            for k2, match in gr.items():
                group[k2] = match
    return
#%% md
# # Pipeline: Image matching
#%%
def exec_feature_extraction(params):
    images = params.images
    feature_dir = params.feature_dir
    device = params.device
    
    t = time()
    index_pairs = get_image_pairs_shortlist(
        images,
        sim_th = CONFIG.sim_th, # should be strict
        min_pairs = CONFIG.min_pairs, # we should select at least min_pairs PER IMAGE with biggest similarity
        exhaustive_if_less = CONFIG.exhaustive_if_less,
        device=device
    )
    params.laptime_image_pairs = time() - t
    params.image_pairs = index_pairs
    print (f'Shortlisting. Number of pairs to match: {len(index_pairs)}. Done in {params.laptime_image_pairs:.4f} sec')
    gc.collect()

    t = time()
    files_keypoints = []
    for i_param, imc_param in enumerate(CONFIG.params_alikedlg):        
        for rot in range(1):
            file_keypoints = f'{feature_dir}/aliked_lightglue_param{i_param}_rot{rot}_mkpts.h5'
            max_num_keypoints = imc_param.max_num_keypoints
            resize_to = imc_param.image_size
            min_matches = imc_param.min_matches
            matching_aliked_lightglue_rot(
                images,
                index_pairs,
                rot,
                file_keypoints,
                feature_dir, 
                max_num_keypoints, 
                resize_to=resize_to,
                device=device,
                min_matches=min_matches,
                verbose=True,
            )
            files_keypoints.append( file_keypoints )
            gc.collect()
    params.laptime_lightglue_4rots = time() - t
    print(f'Features matched in {params.laptime_lightglue_4rots:.4f} sec')

    # RoMa
    """
    t = time()
    file_keypoints = f'{feature_dir}/roma_mkpts.h5'
    matching_roma(
        images,
        index_pairs,
        file_keypoints,
        feature_dir,
        num_features=CONFIG.roma_max_num_keypoints,
        resize_to=CONFIG.roma_image_size,
        device=device,
        min_matches=CONFIG.min_matches,
        verbose=True,
    )
    files_keypoints.append( file_keypoints )
    gc.collect()
    params.laptime_roma = time() - t
    print(f'Features matched in {params.laptime_roma:.4f} sec')
    """
    
    # Merge mkpts and create keypoints/matches
    sleep(10)
    keypoints_merger(
        images,
        index_pairs,
        files_keypoints,
        feature_dir,
        filter_FundamentalMatrix = False,
        filter_iterations = 10,
        filter_threshold = 8,
    )
    
    gc.collect()
    return params
#%% md
# # SfM Maps Merger
#%%
# Merge maps of colmap
import argparse, shutil, subprocess, tempfile, sys
from pathlib import Path

import networkx as nx
import pycolmap  # pip install pycolmap

# ---------- util ----------------------------------------------------------------
def read_image_names(model_dir: Path):
    """
    pycolmap 0.6.x では Reconstruction() で読み込む。
    返り値: 画像ファイル名(set[str])
    """
    rec = pycolmap.Reconstruction(str(model_dir))   # ← これで images.bin をパース
    return {img.name for img in rec.images.values()}

#def read_image_names(model_dir: Path):
#    images = pycolmap.read_images_binary(model_dir / "images.bin")
#    return {img.name for img in images.values()}

def build_overlap_graph(image_sets, min_common):
    G = nx.Graph()
    G.add_nodes_from(range(len(image_sets)))
    for i in range(len(image_sets)):
        for j in range(i + 1, len(image_sets)):
            if len(image_sets[i] & image_sets[j]) >= min_common:
                G.add_edge(i, j)
    return G

def run_cmd(cmd):
    """stdout+stderr をストリーム出力しつつ実行"""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line, end="")
    proc.wait()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)

# ---------- COLMAP wrappers ------------------------------------------------------
def merge_two_models(colmap_bin, ref_model, src_model, out_dir):
    cmd = [
        colmap_bin, "model_merger",
        "--input_path1", str(ref_model),
        "--input_path2", str(src_model),
        "--output_path", str(out_dir),
    ]
    try:
        run_cmd(cmd)
        return True
    except subprocess.CalledProcessError:
        return False

def run_bundle_adjuster(colmap_bin, model_dir, num_threads=-1):
    """
    実行例:
        colmap bundle_adjuster --input_path scene_000 --output_path scene_000 \
            --BundleAdjustment.refine_principal_point 1
    """
    cmd = [
        colmap_bin, "bundle_adjuster",
        "--input_path", str(model_dir),
        "--output_path", str(model_dir),
        "--BundleAdjustment.refine_focal_length", "1",
        "--BundleAdjustment.refine_principal_point", "1",
        "--BundleAdjustment.refine_extra_params", "1",
    ]
    if num_threads > 0:
        cmd += ["--Mapper.num_threads", str(num_threads)]
    run_cmd(cmd)     # raise on error

# ---------- main logic -----------------------------------------------------------
def cluster_and_merge(
    model_dirs,
    out_root,
    colmap_bin="colmap",
    min_common=10,
    run_bundle_adjustment=True,
    keep_tmp=False,
):
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    # 1) 画像集合
    image_sets = [read_image_names(Path(m)) for m in model_dirs]

    # 2) 重複グラフ → 連結成分
    clusters = list(nx.connected_components(build_overlap_graph(image_sets, min_common)))
    print(f"num of clusters = {len(clusters)}")
    
    merged_paths = []
    for cidx, comp in enumerate(clusters):
        comp = list(comp)
        if len(comp) == 1:
            src = Path(model_dirs[comp[0]])
            dst = out_root / f"scene_{cidx:03d}"
            shutil.copytree(src, dst, dirs_exist_ok=True)
            merged_paths.append(dst)
            if run_bundle_adjustment:
                run_bundle_adjuster(colmap_bin, dst)
            continue

        # 3) 画像数の多い順に
        comp_sorted = sorted(comp, key=lambda i: len(image_sets[i]), reverse=True)
        work_dir = Path(model_dirs[comp_sorted[0]])

        # 4) 順次マージ
        failed_sources = []
        for midx in comp_sorted[1:]:
            tmp_dir = Path(tempfile.mkdtemp(prefix=f"merge_s{cidx}_"))
            ok = merge_two_models(colmap_bin, work_dir, Path(model_dirs[midx]), tmp_dir)
            if ok:
                work_dir = tmp_dir
            else:
                failed_sources.append(midx)

        # 5) 出力 & BA
        final_dir = out_root / f"scene_{cidx:03d}"
        shutil.move(str(work_dir), final_dir)
        merged_paths.append(final_dir)

        if run_bundle_adjustment:
            run_bundle_adjuster(colmap_bin, final_dir)

        # 6) マージ失敗分を別シーンとしてコピー
        for fidx in failed_sources:
            dst = out_root / f"scene_{cidx}_{fidx}"
            shutil.copytree(model_dirs[fidx], dst, dirs_exist_ok=True)
            merged_paths.append(dst)
            if run_bundle_adjustment:
                run_bundle_adjuster(colmap_bin, dst)

    return merged_paths
#%% md
# # Update submission values
#%%
def update_prediction(params, result_map_dirs, retry):
    # Parse
    feature_dir = params.feature_dir
    images_dir = params.images_dir
    filename_to_index = params.filename_to_index
    predictions = params.predictions
    dataset = params.dataset

    maps = {}
    for idx, result_map_dir in enumerate(result_map_dirs):
        maps[idx] = pycolmap.Reconstruction(result_map_dir)
    
    print ("Counting map size...")
    list_num_images = []
    if isinstance(maps, dict):
        for idx1, rec in maps.items():
            list_num_images.append( len(rec.images) )
    list_num_images = np.array(list_num_images)
    print(f"list_num_images = {list_num_images}")
    if params.list_model_size is None:
        params.list_model_size = [list_num_images]
    else:
        params.list_model_size.append( list_num_images )
    sort_idx = np.argsort( np.array(list_num_images) )
    
    registered = 0
    for map_index, cur_idx in enumerate(sort_idx):
        cur_map = maps[cur_idx]
        cur_map_size = list_num_images[cur_idx]
        if cur_map_size < 4:
            continue
        for index, image in cur_map.images.items():
            prediction_index = filename_to_index[image.name]
            if (cur_map_size > predictions[prediction_index].map_size) and (cur_map_size > 5):
                predictions[prediction_index].map_size = cur_map_size
                predictions[prediction_index].cluster_index = map_index
                predictions[prediction_index].retry_index = retry
                predictions[prediction_index].rotation = deepcopy(image.cam_from_world.rotation.matrix())
                predictions[prediction_index].translation = deepcopy(image.cam_from_world.translation)
                registered += 1
    del maps
    gc.collect()
    return params
#%% md
# # Clustering
#%%
import networkx as nx
from networkx.algorithms.community import louvain_communities
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from typing import List, Tuple, Iterable

def get_network_from_matches_h5( file, images, num_max_keypoints = 8192, th_matches=150):
    image_to_index = {file:i for i,file in enumerate(images)}
    index_to_image = {i:file for i,file in enumerate(images)}

    edges = []
    with h5py.File(file, "r") as f_mat:
        for key1 in f_mat.keys():
            for key2 in f_mat[key1].keys():
                if f_mat[ key1 ][ key2 ].shape[0] >=th_matches:
                    edges.append( (key1, key2, f_mat[key1][key2].shape[0] / num_max_keypoints) )
    G = nx.Graph()
    G.add_weighted_edges_from(edges, weight="weight")
    return G, image_to_index, index_to_image

def get_components(
    G: nx.Graph | nx.DiGraph,
    *,
    directed_mode: str = "auto"  # "auto" | "weak" | "strong"
) -> Tuple[int, List[List]]:
    # --- 無向グラフ ----------------------------------------------------
    if not G.is_directed():
        comp_iter: Iterable[set] = nx.connected_components(G)

    # --- 有向グラフ ----------------------------------------------------
    else:
        if directed_mode == "strong":
            comp_iter = nx.strongly_connected_components(G)
        elif directed_mode in {"weak", "auto"}:
            comp_iter = nx.weakly_connected_components(G)
        else:
            raise ValueError("directed_mode must be 'auto', 'weak', or 'strong'")

    components = [sorted(list(c)) for c in comp_iter]
    n_components = len(components)
    return n_components, components

def get_scenes_from_graph(G, random_state=42, th=0.2):
    communities = louvain_communities(
        G,
        weight="weight",
        resolution=th,
        seed=random_state
    )
    
    scenes = []
    print(f"#clusters = {len(communities)}")
    for cid, members in enumerate(communities):
        scene = set(members)
        print(f"Cluster {cid}: {len(members)} | {sorted(members)}")
        if len(scene) >= 5:
            scenes.append( scene )
        print("="*50)
    return scenes
#%% md
# # Pipeline: Multi-Scene SfM
#%%
def exec_reconstruction(params):
    feature_dir = params.feature_dir
    params.laptime_calc_fmat = []
    params.laptime_sfm = []

    # Clustering
    feature_dir = params.feature_dir
    fnames = [ p.filename for p in params.predictions ]

    matches_file = f'{feature_dir}/matches.h5'
    scenes = []
    num_retry = 4
    for _ in range(num_retry):
        G, images_to_index, index_to_image = get_network_from_matches_h5( 
            matches_file, fnames, num_max_keypoints = 8192, th_matches=150,
        )
        n_components, components = get_components(G)
        for component in components:
            if len(component) > 4:
                scenes.append( set(component) )

    # SfM for each scne cluster
    for retry, scene in enumerate(scenes):
        params = reconstruction_single(params, scene, retry, 2)

    # merge models
    input_map_dirs = sorted( glob.glob( f"{feature_dir}/colmap_rec_*/*/cameras.bin"))
    input_map_dirs = [ 
        os.path.dirname(x)
        for x in input_map_dirs
        if len(pycolmap.Reconstruction( os.path.dirname(x) ).images) > 8
    ]
    input_map_dirs = [ 
        x 
        for x in input_map_dirs
        if pycolmap.Reconstruction(x).compute_mean_reprojection_error() < 2.0
    ]

    if len(input_map_dirs) > 1:
        output_dir = f"{feature_dir}/colmap_rec_merged/"
        COLMAP_BIN = "/usr/bin/colmap"
        MERGE_MIN_COMMON = 6
        MERGE_RUN_BA = True
        result_map_dirs = cluster_and_merge(
            input_map_dirs,
            output_dir,
            colmap_bin=COLMAP_BIN,
            min_common=MERGE_MIN_COMMON,
            run_bundle_adjustment=MERGE_RUN_BA,
            keep_tmp=False,
        )
    
        # update motion info
        update_prediction(params, result_map_dirs, len(scenes) )
    clear_output(wait=False)
    return params

def reconstruction_single(params, scene, retry, min_model_size):
    # Parse
    feature_dir = params.feature_dir
    images_dir = params.images_dir
    filename_to_index = params.filename_to_index
    predictions = params.predictions

    # Execute process
    database_path = os.path.join(feature_dir, f'colmap_{retry}.db')
    if os.path.isfile(database_path):
        os.remove(database_path)
    gc.collect()
    sleep(1)
    #import_into_colmap(images_dir, feature_dir=feature_dir, database_path=database_path)
    import_into_colmap_with_scene(images_dir, scene, feature_dir=feature_dir, database_path=database_path)
    output_path = f'{feature_dir}/colmap_rec_{retry}'
    
    t = time()
    pycolmap.match_exhaustive(database_path)
    params.laptime_calc_fmat = time() - t
    print(f'Ran RANSAC in {params.laptime_calc_fmat:.4f} sec')
    
    # By default colmap does not generate a reconstruction if less than 10 images are registered.
    # Lower it to 3.
    mapper_options = pycolmap.IncrementalPipelineOptions()
    mapper_options.min_model_size = min_model_size #25 # 30 # 20 # 10 # 3
    mapper_options.max_num_models = 15 # 25 # 25

    # Strict initial pairs
    #mapper_options.mapper.init_min_num_inliers = 200 # default:100
    #mapper_options.mapper.init_max_error = 2         # default:4
    #mapper_options.mapper.init_min_tri_angle = 10    # default:16

    ##
    #mapper_options.max_model_overlap = 30 # 20
    #mapper_options.min_num_matches   = 50
    ##
    mapper_options.init_num_trials = 1000 # 200
    
    os.makedirs(output_path, exist_ok=True)
    t = time()
    maps = pycolmap.incremental_mapping(
        database_path=database_path, 
        image_path=images_dir,
        output_path=output_path,
        options=mapper_options)
    sleep(1)
    params.laptime_sfm = time() - t
    print(f'Reconstruction done in  {params.laptime_sfm:.4f} sec')
    print(maps)

    clear_output(wait=False)

    #print("merge maps...")
    #print(f"before: len(maps) = ", len(maps))
    #maps = merge_models_dict(maps)
    #print(f"after: len(maps) = ", len(maps))

    print ("Counting map size...")
    list_num_images = []
    if isinstance(maps, dict):
        for idx1, rec in maps.items():
            list_num_images.append( len(rec.images) )
    list_num_images = np.array(list_num_images)
    print(f"list_num_images = {list_num_images}")
    if params.list_model_size is None:
        params.list_model_size = [list_num_images]
    else:
        params.list_model_size.append( list_num_images )
    sort_idx = np.argsort( np.array(list_num_images) )

    registered = 0
    for map_index, cur_idx in enumerate(sort_idx):
        cur_map = maps[cur_idx]
        cur_map_size = list_num_images[cur_idx]
        for index, image in cur_map.images.items():
            prediction_index = filename_to_index[image.name]
            if (cur_map_size > predictions[prediction_index].map_size) and (cur_map_size > 5):
                predictions[prediction_index].map_size = cur_map_size
                predictions[prediction_index].cluster_index = map_index
                predictions[prediction_index].retry_index = retry
                predictions[prediction_index].rotation = deepcopy(image.cam_from_world.rotation.matrix())
                predictions[prediction_index].translation = deepcopy(image.cam_from_world.translation)
                registered += 1
    gc.collect()

    return params
#%% md
# # Main
#%%
# Collect vital info from the dataset


@dataclasses.dataclass
class Prediction:
    image_id: str | None  # A unique identifier for the row -- unused otherwise. Used only on the hidden test set.
    dataset: str
    filename: str
    map_size: int = -1
    cluster_index: int | None = None
    retry_index: int = -1
    rotation: np.ndarray | None = None
    translation: np.ndarray | None = None

@dataclasses.dataclass
class DatasetParams:
    dataset: str
    feature_dir: str | None = None
    images_dir: str | None = None
    filename_to_index: dict | None = None
    predictions: list | None = None
    images: list | None = None
    device: str | None = None
    laptime_image_pairs: float = -1.0
    laptime_lightglue_4rots: float = -1.0
    laptime_roma: float = -1.0
    laptime_calc_fmat: float = -1.0
    laptime_sfm: float = -1.0
    image_pairs: list | None = None
    list_model_size: list | None = None

    def summary(self):
        print("[Summary]")
        print(f"- Dataset                   : {self.dataset}")
        if self.images is not None:
            print(f"- images                    : {len(self.images)}")
        if self.image_pairs is not None:
            print(f"- pairs                     : {len(self.image_pairs)}")
        print(f"- laptime_image_pairs       : {self.laptime_image_pairs:.2f}")
        print(f"- laptime_lightglue_4rots   : {self.laptime_lightglue_4rots:.2f}")
        print(f"- laptime_roma              : {self.laptime_roma:.2f}")
        print(f"- laptime_calc_fmat         : {self.laptime_calc_fmat:.2f}")
        print(f"- laptime_sfm               : {self.laptime_sfm:.2f}")
        print(f"- list_model_size           : {self.list_model_size}")

# Set is_train=True to run the notebook on the training data.
# Set is_train=False if submitting an entry to the competition (test data is hidden, and different from what you see on the "test" folder).
is_train = False
data_dir = '/kaggle/input/image-matching-challenge-2025'
workdir = '/tmp/kaggle/working/result/'

if is_train:
    sample_submission_csv = os.path.join(data_dir, 'train_labels.csv')
else:
    sample_submission_csv = os.path.join(data_dir, 'sample_submission.csv')

samples = {}
dataset_logs = []
competition_data = pd.read_csv(sample_submission_csv)
if (not is_train) and (competition_data.shape[0] == 1945):
    competition_data = competition_data[ competition_data["dataset"].isin(["ETs", "stairs"]) ]
    workdir = '/kaggle/working/result/'

os.makedirs(workdir, exist_ok=True)

for _, row in competition_data.iterrows():
    # Note: For the test data, the "scene" column has no meaning, and the rotation_matrix and translation_vector columns are random.
    if row.dataset not in samples:
        samples[row.dataset] = []
    prediction = Prediction(
        image_id=None if is_train else row.image_id,
        dataset=row.dataset,
        filename=row.image
    )

    #if len(samples[row.dataset]) < 10:
    samples[row.dataset].append( prediction )

for dataset in samples:
    print(f'Dataset "{dataset}" -> num_images={len(samples[dataset])}')
#%%
gc.collect()

max_images = None  # Used For debugging only. Set to None to disable.
datasets_to_process = None  # Not the best convention, but None means all datasets.

if is_train:
    # max_images = 5

    # Note: When running on the training dataset, the notebook will hit the time limit and die. Use this filter to run on a few specific datasets.
    datasets_to_process = [
    	# New data.
    	#'amy_gardens',
    	'ETs',
    	#'fbk_vineyard',
    	'stairs',
    	# Data from IMC 2023 and 2024.
    	# 'imc2024_dioscuri_baalshamin',
    	# 'imc2023_theather_imc2024_church',
    	# 'imc2023_heritage',
    	 'imc2023_haiper',
    	# 'imc2024_lizard_pond',
    	# Crowdsourced PhotoTourism data.
    	# 'pt_stpeters_stpauls',
    	# 'pt_brandenburg_british_buckingham',
    	# 'pt_piazzasanmarco_grandplace',
    	# 'pt_sacrecoeur_trevi_tajmahal',
    ]

mapping_result_strs = []


# Enqeue feature extraction processing
futures_gpu0 = {}
futures_gpu1 = {}
device = None
device_index = None
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executors_gpu0, \
     concurrent.futures.ThreadPoolExecutor(max_workers=1) as executors_gpu1:

    executors_gpus = [executors_gpu0, executors_gpu1]
    futures_gpus = [futures_gpu0, futures_gpu1]
    for dataset, predictions in samples.items():
        if datasets_to_process and dataset not in datasets_to_process:
            print(f'Skipping "{dataset}"')
            continue
        
        images_dir = os.path.join(data_dir, 'train' if is_train else 'test', dataset)
        images = [os.path.join(images_dir, p.filename) for p in predictions]
        if max_images is not None:
            images = images[:max_images]
    
        print(f'\nProcessing dataset "{dataset}": {len(images)} images')
    
        filename_to_index = {p.filename: idx for idx, p in enumerate(predictions)}
    
        feature_dir = os.path.join(workdir, 'featureout', dataset)
        os.makedirs(feature_dir, exist_ok=True)

        # Switch device
        device, device_index = switch_gpu(device, device_index)
        
        # Dataset parameter
        dataset_params = DatasetParams(
            dataset = dataset,
            feature_dir = feature_dir,
            images_dir = images_dir,
            predictions = predictions,
            filename_to_index = filename_to_index,
            images = images,  # image filepaths
            device = device,
        )

        # Enqueue feature extraction
        futures_gpus[device_index][dataset] = executors_gpus[device_index].submit(
            exec_feature_extraction, dataset_params,
        )
        #dataset_params = exec_feature_extraction(dataset_params)

    # Enqeue reconstruction processing
    futures_cpu  = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG.num_pallalel_sfm) as executors:
        for dataset, predictions in samples.items():
            if datasets_to_process and (dataset not in datasets_to_process):
                print(f'Skipping "{dataset}"')
                continue
                
            if dataset in futures_gpu0.keys():
                future = futures_gpu0[dataset]
            else:
                future = futures_gpu1[dataset]
    
            # Wait for feature extraction
            print(f"waiting feature extraction at dataset = {dataset}")
            dataset_params = future.result()
    
            # if feature extraction is failed:
            if dataset_params is None:
                continue
                
            # Enqueue reconstruction
            gc.collect()
            futures_cpu[dataset] = executors.submit(
                exec_reconstruction, dataset_params,
            )

        # Wait to reconstruction
        for dataset, predictions in samples.items():
            if datasets_to_process and (dataset not in datasets_to_process):
                print(f'Skipping "{dataset}"')
                continue
            gc.collect()
            dataset_params = futures_cpu[dataset].result()
            samples[dataset] = dataset_params.predictions
            dataset_logs.append( dataset_params )
            gc.collect()
#%% md
# ## Create submission
#%%
# Must Create a submission file.

array_to_str = lambda array: ';'.join([f"{x:.09f}" for x in array])
none_to_str = lambda n: ';'.join(['nan'] * n)

submission_file = '/kaggle/working/submission.csv'
with open(submission_file, 'w') as f:
    if is_train:
        f.write('dataset,scene,image,rotation_matrix,translation_vector\n')
        for dataset in samples:
            for prediction in samples[dataset]:
                cluster_name = 'outliers' if prediction.cluster_index is None else f'retry{prediction.retry_index}cluster{prediction.cluster_index}'
                rotation = none_to_str(9) if prediction.rotation is None else array_to_str(prediction.rotation.flatten())
                translation = none_to_str(3) if prediction.translation is None else array_to_str(prediction.translation)
                f.write(f'{prediction.dataset},{cluster_name},{prediction.filename},{rotation},{translation}\n')
    else:
        f.write('image_id,dataset,scene,image,rotation_matrix,translation_vector\n')
        for dataset in samples:
            for prediction in samples[dataset]:
                cluster_name = 'outliers' if prediction.cluster_index is None else f'retry{prediction.retry_index}cluster{prediction.cluster_index}'
                rotation = none_to_str(9) if prediction.rotation is None else array_to_str(prediction.rotation.flatten())
                translation = none_to_str(3) if prediction.translation is None else array_to_str(prediction.translation)
                f.write(f'{prediction.image_id},{prediction.dataset},{cluster_name},{prediction.filename},{rotation},{translation}\n')

!head {submission_file}
#%% md
# # Running logs
#%%
for dataset_params in dataset_logs:
    print("=" * 100)
    dataset_params.summary()
#%% md
# # CV scoring
#%%
# Definitely Compute results if running on the training set.
# Do not do this when submitting a notebook for scoring. All you have to do is save your submission to /kaggle/working/submission.csv.

if is_train:
    t = time()
    final_score, dataset_scores = metric.score(
        gt_csv='/kaggle/input/image-matching-challenge-2025/train_labels.csv',
        user_csv=submission_file,
        thresholds_csv='/kaggle/input/image-matching-challenge-2025/train_thresholds.csv',
        mask_csv=None if is_train else os.path.join(data_dir, 'mask.csv'),
        inl_cf=0,
        strict_cf=-1,
        verbose=True,
    )
    print(f'Computed metric in: {time() - t:.02f} sec.')
#%%
