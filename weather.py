from toolz import concat, memoize, reduce
from functools import lru_cache
from scipy.stats import beta
import numpy as np
import gym


N_SAMPLE = 10000

def memo_key(args, kwargs):
    """Symmetry breaking hashing."""
    env = args[0]
    state = args[1]
    if len(args) > 2:
        action = args[2]
        mask = [0] * len(state)
        mask[action] = 1
        state = zip(state, mask)
        state = ((s, i == action) for i, s in enumerate(state))
    # return sum(map(hash, map(str, state)))
    return tuple(sorted(state))


class TornadoEnv(gym.Env):
    """Decide whether or not to evacuate each city."""
    term_state = '__term_state__'

    def __init__(self, n_city, max_sims, evac_cost=1, false_neg_cost=20, sim_cost=0, prior=(.1, .9)):
        super().__init__()
        self.n_city = self.n_arm = n_city
        self.max_sims = max_sims
        self.evac_cost = -abs(evac_cost)
        self.false_neg_cost = -abs(false_neg_cost)
        self.sim_cost = -abs(sim_cost)
        self.prior = prior
        self.prior_dist = beta(*prior)

        self.init = (prior,) * n_city
        self._cities = range(n_city)
        self._actions = range(n_city + 1)
        self.term_action = self._actions[-1]
        self._max_sum = max_sims + sum(concat(self.init))
        self._reset()
        self.n_actions = n_city + 1

    def __hash__(self):
        return hash((self.n_city, self.evac_cost, self.false_neg_cost,
                     self.sim_cost, self.max_sims, self.prior))

    def _reset(self):
        self._state = self.init
        self.true_p = self.prior_dist.rvs(self.n_city)
        return self._state

    def _step(self, action):
        if action == self.term_action:
            # r = self.expected_term_reward(self._state)
            r = self.true_term_reward(self._state)
            return self.term_state, r, True, {}
        else:
            city = action
            p = self.true_p[city]
            
            s = list(self._state)
            a, b = s[city]
            if np.random.rand() < p:
                s[city] = (a + 1, b)
            else:
                s[city] = (a, b + 1)
            self._state = tuple(s)

            return self._state, self.sim_cost, False, {}


    def actions(self, state):
        if state is self.term_state:
            return []
        elif sum(concat(state)) == self._max_sum:
            return [self.term_action]
        else:
            return self._actions

    def action_features(self, action, state=None):
        state = state if state is not None else self._state
        if action == self.term_action:
            return np.array([
                0,
                0,
                0,
                0,
                self.expected_term_reward(state)
            ])
        etr = self.expected_term_reward(state)
        return np.array([
            self.sim_cost,
            self.myopic_voc(state, action),
            self.vpi_action(state, action),
            self.vpi(state),
            etr
        ])

    def value(self, state, city):
        a, b = state[city]
        p = a / (a + b)
        return max(p * self.false_neg_cost, self.evac_cost)

    def results(self, state, action):
        if action == self.term_action:
            yield (1, self.term_state, self.expected_term_reward(state))
        else:
            city = action
            a, b = state[city]
            p = a / (a + b)

            s = list(state)
            s[city] = (a + 1, b)
            yield (p, tuple(s), self.sim_cost)
            s[city] = (a, b + 1)
            yield (1 - p, tuple(s), self.sim_cost)
    
    @memoize(key=memo_key)
    def expected_term_reward(self, state):
        return sum(self.value(state, a) for a in self._cities)


    def true_term_reward(self, state):
        return sum(self.evac_cost if evac else p * self.false_neg_cost
                   for p, evac in zip(self.true_p, self.decisions(state)))

    def decisions(self, state):
        return [self.value(state, i) == self.evac_cost
                for i in range(self.n_city)]
    
    @memoize(key=memo_key)
    def myopic_voc(self, state, action):
        val = sum(p * self.expected_term_reward(s1)
                  for p, s1, r in self.results(state, action))
        return val - self.expected_term_reward(state)
    
    @memoize(key=memo_key)
    def vpi(self, state):
        return sum(self.vpi_action(state, a) for a in self._actions[:-1])    
    
    @memoize(key=memo_key)
    def vpi_action(self, state, action):
        a, b = state[action]
        fnc = self.false_neg_cost
        val = fnc * expected_min_beta_constant(a, b, self.evac_cost / fnc)
        return val - self.value(state, action)


@lru_cache(None)
def expected_min_beta_constant(a, b, c):
    return np.minimum(_beta_samples(a, b), c).mean()

@lru_cache(None)
def _beta_samples(a, b):
    return beta(a, b).rvs(N_SAMPLE)

@lru_cache(None)
def beta_samples(a, b, idx):
    samples = _beta_samples(a, b).copy()
    np.random.shuffle(samples)
    return samples
