import itertools
import math
import random

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import trange

from .alias import alias_sample, create_alias_table
from .utils import partition_num


class RandomWalker:
    def __init__(self, G, p=1, q=1, use_rejection_sampling=0):
        """
        :param G:
        :param p: Return parameter,controls the likelihood of immediately revisiting a node in the walk.
        :param q: In-out parameter,allows the search to differentiate between “inward” and “outward” nodes
        :param use_rejection_sampling: Whether to use the rejection sampling strategy in node2vec.
        """
        self.G = G
        self.p = p
        self.q = q
        self.use_rejection_sampling = use_rejection_sampling

    def deepwalk_walk(self, walk_length, start_node):

        walk = [start_node]

        while len(walk) < walk_length:
            cur = walk[-1]
            cur_nbrs = list(self.G.neighbors(cur))
            if len(cur_nbrs) > 0:
                walk.append(random.choice(cur_nbrs))
            else:
                break
        return walk

    def node2vec_walk(self, walk_length, start_node):

        G = self.G
        alias_nodes = self.alias_nodes
        alias_edges = self.alias_edges

        walk = [start_node]

        while len(walk) < walk_length:
            cur = walk[-1]
            cur_nbrs = list(G.neighbors(cur))
            if len(cur_nbrs) > 0:
                if len(walk) == 1:
                    walk.append(
                        cur_nbrs[alias_sample(alias_nodes[cur][0], alias_nodes[cur][1])])
                else:
                    prev = walk[-2]
                    edge = (prev, cur)
                    next_node = cur_nbrs[alias_sample(alias_edges[edge][0],
                                                      alias_edges[edge][1])]
                    walk.append(next_node)
            else:
                break

        return walk

    def node2vec_walk2(self, walk_length, start_node):
        """
        Reference:
        KnightKing: A Fast Distributed Graph Random Walk Engine
        http://madsys.cs.tsinghua.edu.cn/publications/SOSP19-yang.pdf
        """

        def rejection_sample(inv_p, inv_q, nbrs_num):
            upper_bound = max(1.0, max(inv_p, inv_q))
            lower_bound = min(1.0, min(inv_p, inv_q))
            shatter = 0
            second_upper_bound = max(1.0, inv_q)
            if (inv_p > second_upper_bound):
                shatter = second_upper_bound / nbrs_num
                upper_bound = second_upper_bound + shatter
            return upper_bound, lower_bound, shatter

        G = self.G
        alias_nodes = self.alias_nodes
        inv_p = 1.0 / self.p
        inv_q = 1.0 / self.q
        walk = [start_node]
        while len(walk) < walk_length:
            cur = walk[-1]
            cur_nbrs = list(G.neighbors(cur))
            if len(cur_nbrs) > 0:
                if len(walk) == 1:
                    walk.append(
                        cur_nbrs[alias_sample(alias_nodes[cur][0], alias_nodes[cur][1])])
                else:
                    upper_bound, lower_bound, shatter = rejection_sample(
                        inv_p, inv_q, len(cur_nbrs))
                    prev = walk[-2]
                    prev_nbrs = set(G.neighbors(prev))
                    while True:
                        prob = random.random() * upper_bound
                        if (prob + shatter >= upper_bound):
                            next_node = prev
                            break
                        next_node = cur_nbrs[alias_sample(
                            alias_nodes[cur][0], alias_nodes[cur][1])]
                        if (prob < lower_bound):
                            break
                        if (prob < inv_p and next_node == prev):
                            break
                        _prob = 1.0 if next_node in prev_nbrs else inv_q
                        if (prob < _prob):
                            break
                    walk.append(next_node)
            else:
                break
        return walk

    def simulate_walks(self, num_walks, walk_length, workers=1, verbose=0):

        G = self.G

        nodes = list(G.nodes())

        results = Parallel(n_jobs=workers, verbose=verbose, )(
            delayed(self._simulate_walks)(nodes, num, walk_length) for num in
            partition_num(num_walks, workers))

        walks = list(itertools.chain(*results))

        return walks

    def _simulate_walks(self, nodes, num_walks, walk_length,):
        walks = []
        for _ in range(num_walks):
            random.shuffle(nodes)
            for v in nodes:
                if self.p == 1 and self.q == 1:
                    walks.append(self.deepwalk_walk(
                        walk_length=walk_length, start_node=v))
                elif self.use_rejection_sampling:
                    walks.append(self.node2vec_walk2(
                        walk_length=walk_length, start_node=v))
                else:
                    walks.append(self.node2vec_walk(
                        walk_length=walk_length, start_node=v))
        return walks

    def get_alias_edge(self, t, v):
        """
        compute unnormalized transition probability between nodes v and its neighbors give the previous visited node t.
        :param t:
        :param v:
        :return:
        """
        G = self.G
        p = self.p
        q = self.q

        unnormalized_probs = []
        for x in G.neighbors(v):
            weight = G[v][x].get('weight', 1.0)  # w_vx
            if x == t:  # d_tx == 0
                unnormalized_probs.append(weight/p)
            elif G.has_edge(x, t):  # d_tx == 1
                unnormalized_probs.append(weight)
            else:  # d_tx > 1
                unnormalized_probs.append(weight/q)
        norm_const = sum(unnormalized_probs)
        normalized_probs = [
            float(u_prob)/norm_const for u_prob in unnormalized_probs]

        return create_alias_table(normalized_probs)

    def preprocess_transition_probs(self):
        """
        Preprocessing of transition probabilities for guiding the random walks.
        """
        G = self.G
        alias_nodes = {}
        for node in G.nodes():
            unnormalized_probs = [G[node][nbr].get('weight', 1.0)
                                  for nbr in G.neighbors(node)]
            norm_const = sum(unnormalized_probs)
            normalized_probs = [
                float(u_prob)/norm_const for u_prob in unnormalized_probs]
            alias_nodes[node] = create_alias_table(normalized_probs)

        if not self.use_rejection_sampling:
            alias_edges = {}

            for edge in G.edges():
                alias_edges[edge] = self.get_alias_edge(edge[0], edge[1])
                if not G.is_directed():
                    alias_edges[(edge[1], edge[0])] = self.get_alias_edge(edge[1], edge[0])
                self.alias_edges = alias_edges

        self.alias_nodes = alias_nodes
        return


class BiasedWalker:
    def __init__(self, idx2node, temp_path):

        self.idx2node = idx2node
        self.idx = list(range(len(self.idx2node)))
        self.temp_path = temp_path
        pass

    def simulate_walks(self, num_walks, walk_length, stay_prob=0.3, workers=1, verbose=0):

        """
        layers_adj.pkl
        {
            0:
            {
                99: [5, 83, 97, 102, 113, 114, 116, 118, 119, 121, 122, 123, 124, 125, 126, 102, 113, 114, 116, 118, 119, 121, 122, 123, 124, 125, 126, 127, 129, 130, 83, 97, 5],
                5: [99, 102, 113, 114, 116, 118, 119, 121, 122, 123, 124, 125, 126, 127, 129, 130, 83, 97, 83, 97, 99, 102, 113, 114, 116, 118, 119, 121, 122, 123, 124, 125, 126],
                ...,
            },
            ...
            6:
            {
                66: [37, 93, 93, 37],
                37: [66, 93, 66, 93],
                93: [66, 37, 66, 37],
                88: [44, 44],
                44: [88, 88]
            }
        }
        """
        layers_adj = pd.read_pickle(self.temp_path+'layers_adj.pkl')
        """
        {
            0:
            {
                99: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                5: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ...
            },
            ...,
            6:
            {
                66: [2, 0, 1, 2],
                37: [3, 0, 3, 1],
                93: [3, 0, 3, 1],
                88: [0, 0],
                44: [0, 0]
            }
        """
        layers_alias = pd.read_pickle(self.temp_path+'layers_alias.pkl')
        """
        {
            0:
            {
                99: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ...,
                23: [1, 0.673658391251532, 0.6878926193172678, 0.673658391251532, 0.7021268473829972, 0.7163610754487267, 0.673658391251532, 0.673658391251532, 0.673658391251532,...],
            },
            ...
            6:
            {
                66: [3.701252329023336e-138, 1, 0.0, 3.701252329023336e-138],
                37: [2.051729654679691e-259, 1, 2.051729654679691e-259, 0.0],
                93: [1.108667808779786e-121, 1, 1.108667808779786e-121, 0.0],
                88: [1, 1],
                44: [1, 1]
            }
        """
        layers_accept = pd.read_pickle(self.temp_path+'layers_accept.pkl')
        """
        gamma
        {
            0:
            {
                99: 0,
                5: 0,
                83: 0,
                97: 0,
                ...
            },
            1:
            {
                100: 15,
                23: 11,
                33: 11,
                39: 13,
                ...
            },
            ...
            6:
            {
                66: 2,
                37: 2,
                93: 2,
                88: 2,
                44: 2
            }
        }
        """
        gamma = pd.read_pickle(self.temp_path+'gamma.pkl')
        walks = []
        initialLayer = 0

        nodes = self.idx  # list(self.g.nodes()) ,是[0,1,2,3,...,130]

        results = Parallel(n_jobs=workers, verbose=verbose, )(
            # 关键在self._simulate_walks
            delayed(self._simulate_walks)(nodes, num, walk_length, stay_prob, layers_adj, layers_accept, layers_alias, gamma) for num in
            partition_num(num_walks, workers))

        walks = list(itertools.chain(*results))
        return walks

    def _simulate_walks(self, nodes, num_walks, walk_length, stay_prob, layers_adj, layers_accept, layers_alias, gamma):
        walks = []
        for _ in range(num_walks):
            random.shuffle(nodes)
            for v in nodes:
                # 关键在_exec_random_walk
                walks.append(self._exec_random_walk(layers_adj, layers_accept, layers_alias,
                                                    v, walk_length, gamma, stay_prob))
        return walks

        """
        随机游走采样
        采样的主体框架和前面的DeepWalk,Node2Vec差不多，这里就说下不同的地方。 
        由于Struc2Vec是在一个多层图中进行采样，游走可能发生在同一层中，也可能发生跨层，所以要添加一些跨层处理的逻辑。
        """
    def _exec_random_walk(self, graphs, layers_accept, layers_alias, v, walk_length, gamma, stay_prob=0.3):
        initialLayer = 0
        layer = initialLayer

        path = []
        path.append(self.idx2node[v])

        while len(path) < walk_length:
            r = random.random()
            if(r < stay_prob):  # same layer
                # 同层逻辑关键在chooseNeighbor
                v = chooseNeighbor(v, graphs, layers_alias,
                                   layers_accept, layer)
                path.append(self.idx2node[v])
            else:  # different layer
                r = random.random()
                try:
                    x = math.log(gamma[layer][v] + math.e)
                    p_moveup = (x / (x + 1))
                except:
                    print(layer, v)
                    raise ValueError()

                if(r > p_moveup):
                    if(layer > initialLayer):
                        layer = layer - 1
                else:
                    if((layer + 1) in graphs and v in graphs[layer + 1]):
                        layer = layer + 1

        # 返回path路径
        return path


def chooseNeighbor(v, graphs, layers_alias, layers_accept, layer):

    v_list = graphs[layer][v]

    # 下一步关键是alias.py的alias_sample方法
    # v_list是个序列，idx返回一个数字，v是一个数字
    # 这两个参数有问题，需要查一下，第一个参数每个都太小，几乎每个都命中，是不是需要归一化一下。第二个参数都是固定值，应该是这样的吗
    idx = alias_sample(layers_accept[layer][v], layers_alias[layer][v])

    v = v_list[idx]
    return v
