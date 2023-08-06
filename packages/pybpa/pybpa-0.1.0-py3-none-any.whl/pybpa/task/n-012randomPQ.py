# -*- coding:utf-8 -*-
"""
# Name:         dlgxa: n_sample-012randomPQ
# Author:       MilkyDesk
# Date:         2022/3/10 16:28
# Description:
#   生成N-0/1/2不同拓扑下的随机出力
1. 超参数配置方法
2. for 拓扑:
       for 出力: 生成新的dat并保存到指定文件夹
"""

# ------------------------- params --------------------------

# ------------------------- params --------------------------
from utils.utils import GenLoadGenerator, topo_gl_generator
import numpy as np
from dat.bpa_dat import DAT
import networkx as nx
import os

# # 模板dat，里面的数据会变的
# temp_dat = DAT.build_from_folder(template_dat_folder_path)
#
# # 变拓扑，使用branch_index索引
# # 0. 根据dat.branch建立本过程需要使用的数据结构
# branch_bus_order = temp_dat.branch_bus_order
# branch_used = np.ones(len(temp_dat.branch), dtype=np.bool_)
# graph = np.zeros(len(temp_dat.bus))
# for b in branch_bus_order:
#     graph[b[0]] += 1
#     graph[b[1]] += 1
# graph = nx.Graph()
# graph.add_edges_from(branch_bus_order)
#

# gl_iter = GenLoadGenerator(n_sample=1, linked_dat=temp_dat,
#                            load=True, load_q=True, gen=True, gen_v=False,
#                            std=0.1,
#                            zero_correct=True,
#                            gen_load_balance=True,
#                            sampler='lhs')
# topo_gl_generator(k=0, max_k=1, prefix=[],
#                   temp_dat=temp_dat,
#                   branch_used=branch_used, graph=graph, branch_bus_order=branch_bus_order,
#                   dat_iter=gl_iter, target_root_path=target_root_path)

pqpqvt = np.zeros([6, 39], dtype=np.bool_)
pqpqvt[2, 29:31] = True
dat_path = r'E:\Data\transient_stability\39\39节点风机01.dat'
dat = DAT.build_from(dat_path)
generator = LHSGenerator(dat, pqpqvt, 0.2, truncate=0.9973)  # 3sigma
topo_generator(0, dat, r'E:\Data\transient_stability\39\lhs_12/', 20, generator)

