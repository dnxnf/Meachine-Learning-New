#%% md
# # Test Data Leak - LB Boost
# This notebook is a fork of Vladimir's notebook [here][1]. Please upvote his original notebook.
# 
# In Kaggle's OTTO ¨C Multi-Objective Recommender System Competition, we are given both the train data (from present) and the test data (from future). The test data contains partial sequences of sessions. Therefore we can use these partial sequences to train our models in addition to using the train data. In this notebook we begin with Vladimir's Co-visitation Matrix notebook [here][1] and add test data to the training data. We make one change to his code below. Where he loads train parquets with `'../input/otto-chunk-data-inparquet-format/train_parquet/*'` , we change this to include test with `'../input/otto-chunk-data-inparquet-format/*_parquet/*'`.
# 
# This is an experiment to see if using test data during training will boost LB score. The original notebook achieved LB 0.539. Let's see what this notebook achieves. UPDATE: Experiment was successful and boosted LB `+0.003`, so it works!
# 
# ![](https://raw.githubusercontent.com/cdeotte/Kaggle_Images/main/Nov-2022/leak.png)
# 
# Note this method of using test data cannot be used in real life because some of the data we are training with occurs in the future of some of the inference data. The inference test data is from a one week period. Therefore when we infer events occurring the first day of the week, we have the advantage of using events occurring in the last 6 days of the week which is impossible in real life. Discussion [here][3]
# 
# # Notes
# Version 1 confirms that using leaky test data during training boosts our LB score. We will now try some additional experiments to boost LB with co-visitation matrix. The best way to experiment is to set up a local CV scheme and try experiments on local CV. But just for fun, I will try a few experiments directly on LB. The details of the experiments are explained below. Let's see how they perform on LB...
# 
# * **Version 0 LB 0.539** Original notebook using only train data (and no test data).
# * **Version 1 LB 0.541** Train with both test and train data. Boost LB from 0.539 to 0.541. So using test data helps!
# * **Version 2 LB 0.541** Train with test data as weight 2 and train data weight 1 via modifying `all_pairs[aid1][aid2] +=w`. LB slightly better.
# * **Version 3 LB 0.546** Train data plus test data spans 5 weeks. Use weight 4 for most recent data and weight 1 for least recent with formula: `w = 1 + 3*(ts - 1659304800025)/(1662328791563-1659304800025)`. We also remove duplicate recommendations from prediction using `set` on `tail(20)`. Achieved LB 0.546!
# * **Version 4 LB 0.556** Same as version 3 except we use top40. And we remove duplicate recommendations more efficiently using `list(dict.fromkeys(AIDS[::-1]))` trick from Radek1 notebook [here][2]. Achieved LB 0.556!
# * **Version 5** Has BUG, please ignore
# * **Version 6 LB 0.555** Same as version 4 except use equal weight for train and test data. I'm curious if unequal weight is helping or not. I think most of the boost between version 4 and version 1 is because of removing duplicates during inference. (Using top40 instead of top20 only boosts `+0.001`). Let's see how equal weights does. UPDATE: using weights introduced in version 3 boost `+0.001`.
# * **Version 7 LB 0.557** In this experiment, we make Co-visitation Matrices for each type. When making Co-visitation matrix for type "orders" we boost weight of pair to w=5 when second item is an "order". For "carts", we boost to w=5. For "clicks" we do not boost. UPDATE: it boost LB `+0.001`.
# * **Version 8 LB 0.550** Since version 7 seemed to work, in this experiment, for "orders" top40 we use w=100 for "order" and w=10 for "cart". Then for "carts" top40 we use w=10 for "order" and w=100 for "cart". For "clicks" top40 we use w=1 for all. We also add our time weight from version 3. UPDATE: it hurt LB `-0.006`.
# * **Version 9 LB 562** We will use a suggestion from Sinan Calisir in the comments. When inferring test data we will sort by `session` and `ts` but not `type` before groupby apply. Let's try this with our best version 7 notebook. Woohoo! It achieved LB 0.562! Thanks Sinan!
# * **Version 10 LB ???** We will try one more time to adjust the weights of "orders" and "carts". For the "order" top40 we will use w=10. And for the "cart" top40 we will use w=4. For "clicks" w=1. We will also use time weight from version 3. Let's see how this does...
# 
# Note if we had a local CV, then we could set up a grid search and find the optimal weights to use with our co-visitation matrix (with regard to importance of time, clicks, orders, carts and whatever else we can think of). And we could quickly find what other modifications can boost our model's performance.
# 
# [1]: https://www.kaggle.com/code/vslaykovsky/co-visitation-matrix
# [2]: https://www.kaggle.com/code/radek1/co-visitation-matrix-simplified-imprvd-logic
# [3]: https://www.kaggle.com/competitions/otto-recommender-system/discussion/363939
#%% md
# # OTTO: Co-visitation Matrix
# 
# There exist products that are frequently viewed and bought together. Here we leverage this idea by computing a co-visitation matrix of products. It's done in the following way:
# 
# 1. First we look at all pairs of events within the same session that are close to each other in time (< 1 day). We compute co-visitation matrix $M_{aid1,aid2}$ by counting global number of event pairs for each pair across all sessions.
# 2. For each $aid1$ we find top 20 most frequent aid2:  `aid2=argsort(M[aid])[-20:]`
# 3. We produce test results by concatenating `tail(20)` of test session events (see https://www.kaggle.com/code/simamumu/old-test-data-last-20-aid-get-lb0-947) with the most likely recommendations from co-visitation matrix. These recommendations are generated from session AIDs and `aid2` from the step 2
# 
# 
# **Please, smash that thumbs up button and subscribe if you like this notebook!**
#%% md
# ## Utils, imports
#%%
### import numpy as np
from collections import defaultdict
import pandas as pd
from tqdm.notebook import tqdm
import glob
import numpy as np
import multiprocessing
import os
import pickle

import glob
DEBUG=False   
SAMPLING = 1  # Reduce it to improve performance
#%% md
# TOP_20_CACHE = '../input/otto-pickles/top_40_aids_v4.pkl'
# 
# try:
#     from kaggle_secrets import UserSecretsClient
#     user_secrets = UserSecretsClient()
#     secret_value_0 = user_secrets.get_secret("gcloud")
# 
#     with open('/tmp/json', 'w+') as f:
#         f.write(secret_value_0)
#         
#     !gcloud auth login --cred-file /tmp/json    
#     !gsutil cp gs://nesp/top_20_aids.pkl .        
#         
# except Exception  as ex:
#     pass
#%% md
# ## Generate AID pairs
#%%
import sys
def gen_pairs(df):
    df = df.query('session % @SAMPLING == 0').groupby('session', as_index=False, sort=False).apply(lambda g: g.tail(30)).reset_index(drop=True)
    df = pd.merge(df, df, on='session')
    pairs = df.query('abs(ts_x - ts_y) < 24 * 60 * 60 * 1000 and aid_x != aid_y')[['session', 'aid_x', 'aid_y', 'ts_x', 'type_y']]\
        .drop_duplicates(['session', 'aid_x', 'aid_y'])
    return pairs[['aid_x', 'aid_y', 'ts_x', 'type_y']].values
    

def gen_aid_pairs():
    all_pairs = defaultdict(lambda: Counter())
    with tqdm(glob.glob('../input/otto-chunk-data-inparquet-format/*_parquet/*'), desc='Chunks') as prog:
        with multiprocessing.Pool(4) as p:
            for idx, chunk_file in enumerate(prog):
                chunk = pd.read_parquet(chunk_file)#.drop(columns=['type'])
                pair_chunks = p.map(gen_pairs, np.array_split(chunk.head(100000000 if not DEBUG else 10000), 120))            
                for pairs in pair_chunks:
                    for aid1, aid2, ts, typ in pairs:
                        w = 1 + 3*(ts - 1659304800025)/(1662328791563-1659304800025)
                        # HERE WE CAN BOOST WEIGHT, i.e. IF TYP=="ORDERS": W *= 10.0
                        # THEN SAVE THIS MATRIX AS THE "ORDERS" MATRIX
                        # WE CAN MAKE 3 DIFFERENT CO-VISITATION MATRICES
                        all_pairs[aid1][aid2] +=w 
                prog.set_description(f'Mem: {sys.getsizeof(object) // (2 ** 20)}MB')

                if DEBUG and idx >= 2:
                    break
                del chunk, pair_chunks
                gc.collect()
    return all_pairs
        
if os.path.exists(TOP_20_CACHE):
    print('Reading top20 AIDs from cache')
    top_20 = pickle.load(open(TOP_20_CACHE, 'rb'))
else:
    all_pairs = gen_aid_pairs()
    df_top_20 = []
    for aid, cnt in tqdm(all_pairs.items()):
        df_top_20.append({'aid1': aid, 'aid2': [aid2 for aid2, freq in cnt.most_common(20)]})

    df_top_20 = pd.DataFrame(df_top_20).set_index('aid1')
    top_20 = df_top_20.aid2.to_dict()
    import pickle
    with open('top_20_aids.pkl', 'wb') as f:
        pickle.dump(top_20, f)
        
len(top_20)
#%%
for i, (k, v) in enumerate(top_20.items()):
    print(k, v)
    if i > 10:
        break
#%% md
# ## Test set inference
#%%
def load_test():    
    dfs = []
    for e, chunk_file in enumerate(tqdm(glob.glob('../input/otto-chunk-data-inparquet-format/test_parquet/*'))):
        chunk = pd.read_parquet(chunk_file)
        dfs.append(chunk)

    return pd.concat(dfs).reset_index(drop=True).astype({"ts": "datetime64[ms]"})
#%%
test_df = load_test()
#%% md
# import itertools
# 
# def suggest_aids(df):
#     # REMOVE DUPLICATE AIDS AND REVERSE ORDER OF LIST
#     aids = list(dict.fromkeys( df.aid.tolist()[::-1] ))
#     
#     if len(aids) >= 20:
#         # We have enough events in the test session
#         return aids[:20]
#     
#     # Append it with AIDs from the co-visitation matrix. 
#     aids2 = list(itertools.chain(*[top_20[aid] for aid in aids if aid in top_20]))
#     top_aids2 = [aid2 for aid2, cnt in Counter(aids2).most_common(20) if aid2 not in aids]        
#     return list(aids) + top_aids2[:20 - len(aids)]
# 
# ##################
# # BELOW IS CODE ADDED BY CHRIS
# 
# top_20_orders = pickle.load(open('../input/otto-pickles-4/top_40_orders_v12.pkl', 'rb'))
# top_20_carts = pickle.load(open('../input/otto-pickles-4/top_40_carts_v13.pkl', 'rb'))
# 
# def suggest_orders(df):
#     # REMOVE DUPLICATE AIDS AND REVERSE ORDER OF LIST
#     aids = list(dict.fromkeys( df.aid.tolist()[::-1] ))
#     
#     if len(aids) >= 20:
#         # We have enough events in the test session
#         return aids[:20]
#     
#     # Append it with AIDs from the co-visitation matrix. 
#     aids2 = list(itertools.chain(*[top_20_orders[aid] for aid in aids if aid in top_20_orders]))
#     top_aids2 = [aid2 for aid2, cnt in Counter(aids2).most_common(20) if aid2 not in aids]        
#     return list(aids) + top_aids2[:20 - len(aids)]
# 
# def suggest_carts(df):
#     # REMOVE DUPLICATE AIDS AND REVERSE ORDER OF LIST
#     aids = list(dict.fromkeys( df.aid.tolist()[::-1] ))
#     
#     if len(aids) >= 20:
#         # We have enough events in the test session
#         return aids[:20]
#     
#     # Append it with AIDs from the co-visitation matrix. 
#     aids2 = list(itertools.chain(*[top_20_carts[aid] for aid in aids if aid in top_20_carts]))
#     top_aids2 = [aid2 for aid2, cnt in Counter(aids2).most_common(20) if aid2 not in aids]        
#     return list(aids) + top_aids2[:20 - len(aids)]
#%%
pred_df = test_df.sort_values(["session", "ts"]).groupby(["session"]).apply(
    lambda x: suggest_aids(x)
)

##################
# BELOW IS CODE ADDED BY CHRIS

pred_df_orders = test_df.sort_values(["session", "ts"]).groupby(["session"]).apply(
    lambda x: suggest_orders(x)
)

pred_df_carts = test_df.sort_values(["session", "ts"]).groupby(["session"]).apply(
    lambda x: suggest_carts(x)
)
#%%
clicks_pred_df = pd.DataFrame(pred_df.add_suffix("_clicks"), columns=["labels"]).reset_index()
orders_pred_df = pd.DataFrame(pred_df_orders.add_suffix("_orders"), columns=["labels"]).reset_index()
carts_pred_df = pd.DataFrame(pred_df_carts.add_suffix("_carts"), columns=["labels"]).reset_index()
#%%
pred_df
#%%
pred_df = pd.concat(
    [clicks_pred_df, orders_pred_df, carts_pred_df]
)
pred_df.columns = ["session_type", "labels"]
pred_df["labels"] = pred_df.labels.apply(lambda x: " ".join(map(str,x)))
pred_df.to_csv("submission.csv", index=False)