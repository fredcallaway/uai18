#!/usr/bin/env python3

import numpy as np
import pandas as pd
from weather import TornadoEnv
from evaluation import get_util
from exact import solve
from joblib import Parallel, delayed
import joblib
from contexttimer import Timer
from scipy.optimize import minimize_scalar
from policies import LiederPolicy, FunctionPolicy
import os
from agents import Agent


from policies import Policy
class NoMetareasonPolicy(Policy):
    """Distributes computations uniformly"""

    def act(self, state):
        if len(self.env.actions(state)) == 1:
            return self.env.term_action
        else:
            return min(range(len(state)), key=lambda i: sum(state[i]))


def train_policy(n_city, max_sims, N=5000):
    env = TornadoEnv(n_city, max_sims)
    envs = [env] * N
    os.makedirs('data/weather/opt_results/', exist_ok=True)
    fn = f'data/weather/opt_results/{n_city}_{max_sims}.pkl'

    def loss(x):
        np.random.seed(45)
        return -get_util(LiederPolicy([0, 1, x, 0, 1]), envs)

    with Timer() as t:
        res = minimize_scalar(loss, bracket=(0,20), tol=0.05)
        res.time = t.elapsed
        joblib.dump(res, fn)
    print(f'wrote {fn} in {t.elapsed} seconds')



def simulate(n_city, max_sims, N=5000):
    env = TornadoEnv(n_city, max_sims)
    os.makedirs('data/weather/sims/', exist_ok=True)
    fn = f'data/weather/opt_results/{n_city}_{max_sims}.pkl'

    res = joblib.load(f'data/weather/opt_results/20_50.pkl')
    agents = {'LC': LiederPolicy([0, 1, res.x, 0, 1]),
              'uniform': NoMetareasonPolicy()}

    # if n_city == 3 or max_sims < 25:
    #     with Timer() as t:
    #         Q, V, pi, info = solve(env)
    #         V(env.init)
    #     print(f'exact solution computed in {t.elapsed} seconds')
    #     agents['optimal'] = FunctionPolicy(pi)


    for name, pol in agents.items():
        np.random.seed(45)
        df = pd.DataFrame(Agent(env, pol).run_many(5000, pbar=False))
        df['name'] = name
        df['n_city'] = n_city
        df['max_sims'] = max_sims
        df = df.set_index(['n_city', 'max_sims', 'name'])
        df.to_csv(f'data/weather/sims/{n_city}_{max_sims}_{name}.pkl')
        

    print(f'wrote {fn}')





from utils import dict_product
params = list(dict_product({
    'n_city': [10, 20, 30],
    'max_sims': [1,2,3,4,]
}))

print(f'running {len(params)} simulations')
jobs = [delayed(simulate)(**prm) for prm in params]
Parallel(min(len(jobs), 45))(jobs)

