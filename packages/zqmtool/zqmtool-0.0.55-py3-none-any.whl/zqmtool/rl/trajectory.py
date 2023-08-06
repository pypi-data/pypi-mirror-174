import torch
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

from collections import defaultdict
import matplotlib.patches as patches


def save_traj(collector, output_for_goal_representation_learning):
    goal_id_to_goal_info = output_for_goal_representation_learning['goal_info_dict']
    wall = output_for_goal_representation_learning['wall']
    batch, _ = collector.buffer.sample(batch_size=0)
    s_ids = batch.obs_next.state_id
    g_ids = batch.obs_next.goal_id
    ds = batch.done

    traj_infos = defaultdict(dict)
    for s_id, g_id, d_i in zip(s_ids, g_ids, ds):
        s = output_for_goal_representation_learning['state_set'][s_id]
        if g_id not in traj_infos.keys():
            traj_infos[g_id]['goal_state'] = None
            traj_infos[g_id]['state_visitation'] = np.zeros_like(wall)
        traj_infos[g_id]['goal_state'] = goal_id_to_goal_info[g_id]['goal_state']
        traj_infos[g_id]['state_visitation'][s[0], s[1]] += 1

    return traj_infos


def draw_traj(epoch, mode, collector, output_for_goal_representation_learning, test_env, args):
    cmap_dict = output_for_goal_representation_learning['cmap_dict']
    state_set = output_for_goal_representation_learning['state_set']
    goal_id_to_goal_info = output_for_goal_representation_learning['goal_info_dict']
    wall = output_for_goal_representation_learning['wall']

    traj_info = save_traj(collector=collector,
                          output_for_goal_representation_learning=output_for_goal_representation_learning)


    for cur_goal_id in [elem for elem in goal_id_to_goal_info.keys() if goal_id_to_goal_info[elem]['mode'] == mode]:

        ax = plt.gca()
        ax.axis('off')
        ax.set_aspect('auto')

        cmap = cmap_dict[goal_id_to_goal_info[cur_goal_id]['room_id']]
        heatmap = sns.heatmap(ax=ax, data=traj_info[cur_goal_id]['state_visitation'], cmap=cmap)
        cbar = heatmap.collections[0].colorbar
        cbar.set_ticks([])
        cbar.set_label('state visitation count')

        obs = test_env.reset()
        s_id = obs['state_id']
        init_s = state_set[s_id]
        ax.scatter(init_s[0] + 0.5, init_s[1] + 0.5, marker='s', c='b', s=200)
        for goal_id in traj_info.keys():
            if goal_id != cur_goal_id: continue
            g_s = traj_info[goal_id]['goal_state']
            ax.scatter(g_s[1] + 0.5, g_s[0] + 0.5, marker='*', c='y', s=400)

        for block_pos in np.stack(np.where(wall == 1), axis=-1):
            ax.add_patch(
                patches.Rectangle(xy=(block_pos[1], block_pos[0]), width=1, height=1, facecolor='k', fill=True))

        plt.savefig(os.path.join(args.logdir, f'{epoch}_{mode}_{args.rl}_{args.method}_{cur_goal_id}.png'),
                    bbox_inches='tight')
        plt.close()

