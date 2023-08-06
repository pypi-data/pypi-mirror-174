# -*- coding: utf-8 -*-#
import re

import numpy as np
import subprocess
# from environment.environment import *

# -----------------------------------------------------------
# Name:         utils
# Author:       Jerem
# Date:         2021/2/11
# Description:  
# -----------------------------------------------------------

# ------------------------- fields --------------------------
# 赋值
from bpa_operations.base.bpa_str import bpa_str2float

env = 'milky_desktop'

path_root = 'E:/Data/transient_stability/39/'
"""唯一一个与节点数量有关的路径"""

path_bpa = path_root + 'bpa/'
path_pretreated = path_root + 'pretreated/'

dat_file = path_bpa + '0_100_0/0_100_0.temp_dat'

ignored_suffix_in_bpa_folder = ['.db', '.plog', '.prj', '.txt', '.MRK', '.temp_dat', '.error']

bpa_exe_path = 'D:/OneDrive/桌面/PsdEdit/pfnt.exe'


# ------------------------- fields --------------------------
def read_datNF(dat_file):
    """
    读dat文件 @todo line_data, gen_data似乎没有被用到
    @param dat_file: dat_path + file_name
    @return:
    bus_list, line_list, bus_text, line_text, line_data, gen_list, gen_list, gen_data；
    其中_list维度为3，_text维度为2，_data维度为1
    """

    ignored_bus = ['BJZ500', '-HLZ']  # 为啥

    bus_list = []
    """shape=(n_bus, 3): code, metric_name, base"""

    bus_text = []
    """bus_uid_table, shape=(n_bus, 2): code, metric_name+base"""

    gen_list = []
    """shape=(n_gen, 3): code, metric_name, base"""

    gen_text = []
    """gen_uid_table, shape=(n_gen, 2): code, metric_name+base"""

    line_list = []
    """shape=(n_bus, 8): code, name1, base1, name2, base2, r, x, b/2, k"""

    line_text = []
    """line_uid_table, shape=(n_line, 3): code, bus1:metric_name+base, bus2:metric_name+base"""

    line_data = []
    """line_original_lines, shape=(n_line, 1): dat_file_line of bline"""

    gen_data = []
    """gen_original_lines, shape=(n_gen, 1): dat_file_line of gen"""

    dat_lines = open(dat_file, 'r').readlines()
    for dat_line in dat_lines:
        code = dat_line[0:2]
        bus1_name = dat_line[6:14].strip()

        if code[0] == 'B':  # warning: and line_code != 'BD' 两端直流节点不处理
            base_voltage1 = dat_line[14:18].strip()
            bus_list.append([code, bus1_name, base_voltage1])
            bus_text.append([code, bus1_name + str(float(base_voltage1))])

            if code == 'BQ' or code == 'BS' or (code == 'BE' and dat_line[42:47].split() != []):
                gen_data.append(dat_line)
                gen_text.append([code, bus1_name + str(float(base_voltage1))])
                gen_list.append([code, bus1_name, base_voltage1])

        elif (code[0] == 'L' or code[0] == 'T') and code != 'LD' and code != 'L+' \
                and ignored_bus[0] not in dat_line[19:27].strip() and ignored_bus[1] not in dat_line[19:27].strip():
            line_data.append(dat_line)

            base_voltage1 = dat_line[14:18].strip()
            bus2_name = dat_line[19:27].strip()
            base_voltage2 = dat_line[27:31].strip()
            line_r = bpa_str2float(dat_line[38:44], 5)
            line_x = bpa_str2float(dat_line[44:50], 5)
            # line_g_half = bpa_str2float(dat_line[50:56], 5)
            line_b_half = bpa_str2float(dat_line[56:62], 5)
            if dat_line[62:66].strip() == '':
                line_k = 1
            elif code[0] == 'T ':
                line_k = bpa_str2float(dat_line[67:72], 2) / bpa_str2float(dat_line[62:67], 2)
            elif code[0] == 'TP':  # 移相器支路
                line_k = bpa_str2float(dat_line[62:67], 2)

            line_list.append(
                [code, bus1_name, base_voltage1, bus2_name, base_voltage2, line_r, line_x, line_b_half, line_k])
            line_text.append([code, bus1_name + str(float(base_voltage1)), bus2_name + str(float(base_voltage2))])

    return bus_list, line_list, bus_text, line_text, line_data, gen_text, gen_list, gen_data


def read_pfo(dat_path, bus_dict, need_Y_matrix=True):
    """
    读dat文件得到Y矩阵,读pfo文件得到潮流结果。
    @param dat_path: 需要计算的dat
    @param bus_dict:
    @return:
    [bus_info, line_info], success_bool
    when success_bool is False, the other output is None
    """

    branch_info_start_flag = '* * * *  详细的输出列表  * * * *'
    branch_info_end_flag = '整个系统的数据总结'

    bus_info_start_flag = '*  节点相关数据列表'

    n_bus = len(bus_dict)

    # 读pfo文件,如果没有就生成
    pfo_path = dat_path[:-4] + '.pfo'
    # 注释掉的原因：之前自己一波nt操作，导致已生成的样本都是错的
    # if not os.chn_path.exists(dat_path):
    #     run_pf(dat_path)
    pfo_lines = open(pfo_path, 'r', errors='ignore').readlines()

    # 扫描支路信息
    # TODO 不对称矩阵是不能进行对称正交化的，意味着应用GCN有风险 https://www.zhihu.com/question/308109187
    net_p = np.zeros([n_bus, n_bus])
    net_q = np.zeros([n_bus, n_bus])
    find_flag = False
    for pfo_line in pfo_lines:
        if '不收敛' in pfo_line:
            return None, False
        if not find_flag:
            if branch_info_start_flag in pfo_line:
                find_flag = True
            continue
        if branch_info_end_flag in pfo_line:
            break
        if pfo_line[0] == '\n':
            continue

        if pfo_line[0] != ' ':
            from_bus = bus_dict.get(pfo_line[:8].strip())
        elif pfo_line[7] != ' ':
            line_info = re.sub('[线路充电有无功损耗率]', ' ', pfo_line).split()
            to_bus = bus_dict.get(line_info[0])
            if line_info[2] == 'A':  # 有些行就真的没有A
                line_p = float(line_info[3]) / float(line_info[1])
                line_q = float(line_info[4]) / float(line_info[1])
            else:
                line_p = float(line_info[2]) / float(line_info[1])
                line_q = float(line_info[3]) / float(line_info[1])

            net_p[from_bus][to_bus] = line_p
            net_p[from_bus][from_bus] -= line_p

            net_q[from_bus][to_bus] = line_q
            net_q[from_bus][from_bus] -= line_q
    # TODO 需要补充网络信息检查。 手动检查过了


    # 扫描节点信息
    load_p = np.zeros(n_bus)
    load_q = np.zeros(n_bus)
    bus_qq = np.zeros(n_bus)
    bus_v = np.zeros(n_bus)
    bus_t = np.zeros(n_bus)
    gen_p = np.zeros(n_bus)
    gen_q = np.zeros(n_bus)

    find_flag = -1
    for pfo_line in pfo_lines:
        if find_flag == -1:
            if bus_info_start_flag in pfo_line:
                find_flag = 0
            continue
        if find_flag < 3:  # 信息区延迟4行开始
            find_flag += 1
            continue
        if pfo_line[3] == ' ':  # 信息区结束
            break

        line_info = re.sub('/', ' ', pfo_line).split()
        bus_no = bus_dict.get(line_info[0])
        base_mva = float(line_info[1])
        gen_p[bus_no] = float(line_info[3]) / base_mva
        gen_q[bus_no] = float(line_info[4]) / base_mva
        if pfo_line[97] == 'V' or pfo_line[97] == ' ':
            load_p[bus_no] = float(line_info[5]) / base_mva
            load_q[bus_no] = float(line_info[6]) / base_mva
            bus_qq[bus_no] = float(line_info[9]) / base_mva
        else:
            load_p[bus_no] = float(line_info[6]) / base_mva
            load_q[bus_no] = float(line_info[7]) / base_mva
            bus_qq[bus_no] = float(line_info[10]) / base_mva
        bus_v[bus_no] = float(line_info[-2])
        bus_t[bus_no] = float(line_info[-1])

    _, line_text, _, _, _, _, _, _ = read_datNF(dat_path)
    branch_info = form_Y_matrix(line_text, bus_dict) if need_Y_matrix else {}
    branch_info.update({'net_p': net_p, 'net_q': net_q})
    bus_info = {'mean_lp': load_p, 'load_q': load_q, 'bus_qq': bus_qq,
                'bus_v': bus_v, 'bus_t': bus_t,
                'mean_gp': gen_p, 'gen_q': gen_q}

    return [branch_info, bus_info], True


def run_pf(dat_path):
    """
    谨慎使用。方法有问题，pfo为空。并且运行出错的概率反比于sleep时间。
    @param dat_path:
    @return:
    """
    # 使用call而非Popen：执行完这句再执行下一行
    # try:
    # format = open(path_pretreated2 + 'temp_out.txt', 'w')
    # e = open(path_pretreated2 + 'temp_err.txt', 'w')
    iter_times = subprocess.Popen(bpa_exe_path + ' ' + dat_path)
    # iter_times.kill()
    #     iter_times.wait()
    # finally:
    #     iter_times.kill()
    # 获取输出
    # out = sys.stdout.read()
    # err = sys.stderr.read()
    return iter_times


def form_Y_matrix(branch_list, bus_dict):
    """
    返回y矩阵
    https://www.docin.com/p-36426034.html
    2021年3月20日 经过电力系统分析书确认
    @param branch_list: readNF的line_list
    @param bus_dict:
    @return:
    """
    n_bus = len(bus_dict)
    net_g = np.zeros([n_bus, n_bus])
    net_b = np.zeros([n_bus, n_bus])

    for branch in branch_list:
        from_bus = bus_dict.get(branch[1])
        to_bus = bus_dict.get(branch[3])
        r = branch[5]
        x = branch[6]
        b_half = branch[7]
        k = branch[8]

        g = r / (r ** 2 + x ** 2)
        b = -x / (r ** 2 + x ** 2)

        net_g[from_bus][to_bus] -= (g / k)
        net_b[from_bus][to_bus] -= (b / k)

        net_g[to_bus][from_bus] -= (g / k)
        net_b[to_bus][from_bus] -= (b / k)

        net_g[from_bus][from_bus] += g
        net_b[from_bus][from_bus] += b

        net_g[to_bus][to_bus] += (g / k ** 2)
        net_b[to_bus][to_bus] += (b / k ** 2)

    return {'net_g': net_g, 'net_b': net_b}

# 测试
if __name__ == '__main__':
    print('测试读取pfo')
    bus_list, line_list, bus_text, line_text, _, _, _, _ = read_datNF(dat_file)
    bus_dict = {name[1]: i for i, name in enumerate(bus_list)}
    read_pfo(r'D:\OneDrive\桌面\PsdEdit\0_100_0\0_100_0.temp_dat', bus_dict)
