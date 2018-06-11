#!/usr/bin/env python3

import numpy as np
from joblib import Parallel, delayed, dump, load
from tqdm import tqdm

from oldmouselab import OldMouselabEnv
from exact import solve
from evaluation import get_util, bo_policy

np.random.seed(418)
envs = [OldMouselabEnv(3, 2, quantization=6, cost=0.1) for _ in range(600)]
train_envs, test_envs = envs[:100], envs[100:]
env = train_envs[0]

def hash_state(s):
    return sum(hash(tuple(str(x) for x in s[i: i+env.outcomes]))
                 for i in range(0, len(env.init), env.outcomes))

def optimal_value(i):
    env = test_envs[i]
    Q, V, pi, info = solve(env, hash_state=hash_state)
    return V(env.init)

jobs = tqdm([delayed(optimal_value)(i) for i in range(len(test_envs))])
opt_results = Parallel(20)(jobs)
dump(opt_results, 'results/lc_3_2_8_0.1')

policy, result = bo_policy(train_envs, n_calls=60, return_result=True, n_jobs=20)
dump(policy, 'policies/3-2-8-0.1')

lc_results = get_util(policy, test_envs * 10, return_mean=False, parallel=Parallel(20))
dump(lc_results, 'results/opt_3_2_8_0.1')