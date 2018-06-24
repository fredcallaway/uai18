import os
import numpy as np
import pandas as pd
import sys 
from joblib import Parallel, delayed


if __name__ == '__main__':
	dfs = []
	costs = np.logspace(-4, -1, 7)
	for cost in costs:
		cost_i = np.abs(costs - cost).argmin()
		for n_arm in range(2,6):
			filename = 'data/bandit_dqn/results/dqn_results_'+str(n_arm)+"_"+str(cost_i)+'.h5'
			print(filename)
			store = pd.HDFStore(filename)
			df = store['data']
			store.close()
			print(str(n_arm) +' arms. cost: ' + str(cost) +' reward: ' + str(df.util.mean()))
			dfs.append(df)
	store = pd.HDFStore('data/bandit_dqn/results/dqn_results_combined.h5')
	store['data'] = pd.concat(dfs)
	store.close()

