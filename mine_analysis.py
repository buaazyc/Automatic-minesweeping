import numpy as np
from constant import *
import os


def mine_analysis(sum_board, game_info):
    # MINE,RED_MINE,FLAG三个表示的是雷的位置
    filename = 'result.txt'
    if os.path.exists(filename):
        if os.path.getsize(filename):
            with open(filename, 'r+') as f:
                out_dic = eval(f.readline().strip())  # 文件中game_info信息
                assert type(out_dic) == dict  # 字典格式
                for key in out_dic.keys():
                    out_dic[key] += game_info[key]

                # 胜率
                old_rate = f.readline().strip()
                win_rate = round(out_dic['win_count'] / out_dic['total_count'], 2) * 100

                # 矩阵信息
                old_mine_mat = f.read()
                old_mine_mat = np.mat(old_mine_mat).reshape((BOARD_HEIGHT, BOARD_LENGTH))
                assert type(old_mine_mat) == np.matrix  # 矩阵形式
                old_mine_mat += sum_board
                f.seek(0)
                f.truncate()
                f.write(str(out_dic) + '\n')
                f.write(str(win_rate) + '\n')
                f.write(str(old_mine_mat))
                return

    with open(filename, 'w') as f:
        out_dic = {'total_count': game_info['total_count'],
                   'win_count': game_info['win_count'],
                   'defeat_count': game_info['defeat_count']}
        f.write(str(out_dic) + '\n')
        f.write(str(round(game_info['win_count'] / game_info['total_count'], 2) * 100) + '\n')
        f.write(str(sum_board))
