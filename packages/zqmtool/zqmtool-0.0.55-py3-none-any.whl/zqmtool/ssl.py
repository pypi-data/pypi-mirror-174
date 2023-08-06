import os, sys
sys.path.append(os.path.dirname(__file__))

from copy import deepcopy
from typing import Any, Dict, Optional, Union

from tianshou.data import Batch, ReplayBuffer, to_numpy, to_torch_as
from tianshou.policy import DQNPolicy

import torch
from tianshou.utils.net.common import MLP
import torch.nn as nn
import numpy as np
from torch.nn.functional import softplus
from torch.distributions import Normal, Independent
import torch.nn.functional as F
import math
import random
from itertools import combinations
from other import make_path_if_not_exist
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
import seaborn as sns



def update_beta(method, beta, loss_infomin=None, acc=None, min_val=None):
    def add_beta(beta):
        return min(beta + step_val, max_val)

    def reduce_beta(beta):
        return max(beta - step_val, min_val)

    max_val = 0.1
    min_val = 0.01 if min_val is None else min_val
    step_val = 1e-3

    if method == 'infogoal':
        return add_beta(beta) if acc > 0.98 else reduce_beta(beta)
    elif method == 'infobot':
        return 0.001
    else:
        return beta


def reparameterization(params, z_dim, num_sample=1):
    mu, sigma = params[:, :z_dim], params[:, z_dim:]
    sigma = softplus(sigma) + 1e-3  # Make sigma always positive
    if num_sample == 1:
        z = Independent(Normal(loc=mu, scale=sigma), 1).rsample()
    else:
        z = Independent(Normal(loc=mu, scale=sigma), 1).rsample(sample_shape=(num_sample,))
    return z, mu, sigma


def infomax_loss_fn(z_p0, z_p1, z_n0, z_n1):
    z_pos = F.l1_loss(z_p0, z_p1, reduction='none')
    z_neg = F.l1_loss(z_n0, z_n1, reduction='none')

    z_pos = torch.mean(z_pos, dim=-1)
    z_neg = torch.mean(z_neg, dim=-1)
    loss = torch.exp(z_pos - z_neg)
    loss = torch.mean(loss)

    acc = torch.mean(torch.as_tensor(z_pos < z_neg, dtype=torch.float32))
    return loss, acc


def infomin_loss_fn(mu, std):
    loss = -0.5 * (1 + 2 * std.log() - mu.pow(2) - std.pow(2)).sum(1).mean().div(math.log(2))
    return loss


def draw_emb(net, save_path, output_for_goal_representation_learning, times, device):
    make_path_if_not_exist(os.path.dirname(save_path))

    SMALL_SIZE = 6 * times
    MEDIUM_SIZE = 8 * times

    plt.rc('pdf', fonttype=42)
    plt.rc('ps', fonttype=42)
    plt.rc('font', family='serif')
    plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title

    goal_info_dict = output_for_goal_representation_learning['goal_info_dict']

    cur_goal_ids = []
    cur_goals = []
    cur_colors = []
    cur_modes = []
    for cur_goal_id in goal_info_dict.keys():
        cur_modes.append({'train': 0, 'test': 1}[goal_info_dict[cur_goal_id]['mode']])
        cur_goal_ids.append(cur_goal_id)
        cur_colors.append(goal_info_dict[cur_goal_id]['room_id'])
        cur_goals.append(goal_info_dict[cur_goal_id]['goal'])

    with torch.no_grad():
        cur_goals_th = torch.as_tensor(cur_goals, dtype=torch.float32, device=device)
        z, m, s = net.encode_goal(cur_goals_th, num_sample=100)
        z_orig_shape = z.shape

        cur_colors_for_z = np.asarray(cur_colors)[None, ...].repeat(z_orig_shape[0], axis=0).reshape(-1, 1)
        cur_modes_for_z = np.asarray(cur_modes)[None, ...].repeat(z_orig_shape[0], axis=0).reshape(-1, 1)

        cur_colors_for_m = np.asarray(cur_colors).reshape(-1, 1)
        cur_modes_for_m = np.asarray(cur_modes).reshape(-1, 1)

        z = z.reshape(-1, m.shape[-1]).cpu().numpy()
        z_2d = z if z.shape[-1] == 2 else PCA(n_components=2).fit_transform(z)
        z_2d_w_color = np.concatenate([z_2d, cur_colors_for_z, cur_modes_for_z], axis=-1)
        m_2d = np.mean(z_2d.reshape(z_orig_shape[0], z_orig_shape[1], -1), axis=0)
        m_2d_w_color = np.concatenate([m_2d, cur_colors_for_m, cur_modes_for_m], axis=-1)

    z_pd = pd.DataFrame(z_2d_w_color, columns=['x', 'y', 'room', 'mode'])
    m_pd = pd.DataFrame(m_2d_w_color, columns=['x', 'y', 'room', 'mode'])

    m_pd = m_pd.replace({'mode': {0: 'training', 1: 'test'}})
    m_pd = m_pd.replace({'room': {0: 'A', 1: 'B', 2: 'C', 3: 'D'}})

    ax = plt.gca()
    sns.scatterplot(ax=ax, data=z_pd, x='x', y='y', alpha=0.1, style='mode', hue='room', palette="Set2",
                    legend=False)
    sns.scatterplot(ax=ax, data=m_pd, x='x', y='y', style='mode', hue='room', palette="Set2", legend=False)
    ax.set_aspect('auto')
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()


class Base:

    def __init__(self, net, optim, batch_size, positive_instance_pairs):
        self.net = net
        self.optim = optim
        self.device = net.device
        self.batch_size = batch_size
        self.positive_instance_pairs = positive_instance_pairs
        self.len_positive_instance_pairs = None
        self.pos_pair_set = None
        self.neg_pair_set = None

    def divide_pos_neg_pairs(self, ):
        if (self.len_positive_instance_pairs is not None) and \
                (len(self.positive_instance_pairs) == self.len_positive_instance_pairs):
            return

        self.len_positive_instance_pairs = len(self.positive_instance_pairs)

        # get z_a
        a = []
        for pair in self.positive_instance_pairs:
            a += list(pair)
        a = set(a)

        pos_pair_set = []
        for ai in a:
            pos = []
            for pair in self.positive_instance_pairs:
                if ai in pair:
                    pos += list(pair)
            pos = set(pos)

            for posi in pos:
                pos_pair_set.append([ai, posi])

        neg_pair_set = []
        for pair in combinations(a, 2):
            is_pos = False
            for pos_pair in pos_pair_set:
                if ((pair[0] == pos_pair[0]) and (pair[1] == pos_pair[1])) or (pair[1] == pos_pair[0]) and (
                        pair[0] == pos_pair[1]):
                    is_pos = True
                    break

            if not is_pos:
                neg_pair_set.append(pair)

        self.pos_pair_set = pos_pair_set
        self.neg_pair_set = neg_pair_set

    def forward(self):
        raise NotImplementedError

    def update(self):
        self.optim.zero_grad()
        loss, loss_breakdown = self.forward()
        loss.backward()
        self.optim.step()

        desc = " ".join(['{} {:.3f}'.format(k, v) for k, v in loss_breakdown.items()])
        return desc


class InfoMax(Base):

    def __init__(self, net, optim, batch_size, positive_instance_pairs):
        super().__init__(
            net=net, optim=optim, batch_size=batch_size,
            positive_instance_pairs=positive_instance_pairs
        )

    def forward(self):
        self.divide_pos_neg_pairs()
        if (self.pos_pair_set is None) or \
                ((self.neg_pair_set is None)) or \
                (min(len(self.neg_pair_set), len(self.pos_pair_set)) == 0):
            return {'loss': None}

        num_sample = min(len(self.neg_pair_set), len(self.pos_pair_set))
        pos_pairs = np.asarray(random.sample(self.pos_pair_set, num_sample))
        neg_pairs = np.asarray(random.sample(self.neg_pair_set, num_sample))

        a = torch.as_tensor(self.net.goal_set[pos_pairs[:, 0]], dtype=torch.float32, device=self.net.device)
        b = torch.as_tensor(self.net.goal_set[pos_pairs[:, 1]], dtype=torch.float32, device=self.net.device)
        c = torch.as_tensor(self.net.goal_set[neg_pairs[:, 0]], dtype=torch.float32, device=self.net.device)
        d = torch.as_tensor(self.net.goal_set[neg_pairs[:, 1]], dtype=torch.float32, device=self.net.device)

        abcd = torch.cat([a, b, c, d])
        z_abcd, mu, std = self.net.encode_goal(abcd)
        z_a, z_b, z_c, z_d = torch.chunk(z_abcd, 4)

        loss_infomax, infomax_acc = infomax_loss_fn(z_p0=z_a, z_p1=z_b, z_n0=z_c, z_n1=z_d)

        return {'loss': loss_infomax, 'acc': infomax_acc,
                'mu': mu, 'std': std}


class InfoMin(Base):

    def __init__(self, net, optim, batch_size, positive_instance_pairs):
        super().__init__(
            net=net, optim=optim, batch_size=batch_size,
            positive_instance_pairs=positive_instance_pairs
        )

    def forward(self, mu=None, std=None):

        if mu is None:
            pair = np.asarray(list(self.positive_instance_pairs)).copy()
            np.random.shuffle(pair)
            anc = pair[:self.batch_size, 0]
            pos = pair[:self.batch_size, 1]

            if random.random() < 0.5:
                tmp = anc.copy()
                anc = pos.copy()
                pos = tmp

            anc = torch.as_tensor(self.net.goal_set[anc], dtype=torch.float32,
                                  device=self.net.device)
            pos = torch.as_tensor(self.net.goal_set[pos], dtype=torch.float32,
                                  device=self.net.device)

            z_a, m_a, s_a = self.net.encode_goal(anc)
            with torch.no_grad():
                z_pos, m_p, s_p = self.net.encode_goal(pos)

            mu = torch.cat([m_a, m_p])
            std = torch.cat([s_a, s_p])

        loss = infomin_loss_fn(mu, std)
        return {'loss': loss}
