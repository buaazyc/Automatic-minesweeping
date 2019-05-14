from constant import *
import numpy as np


def win_game(game_info):
    # 执行游戏胜利，并输出战绩等信息
    game_info['win_count'] += 1
    show_record(game_info)


def defeat_game(game_info):
    # 执行游戏失败，并输出战绩等信息
    game_info['DEFEAT'] = True
    game_info['defeat_count'] += 1
    show_record(game_info)


def show_record(game_info):
    # 输出战绩等信息
    print("胜利次数：", game_info['win_count'], "失败次数：", game_info['defeat_count'], "总次数：", game_info['total_count'],
          "胜率：", round(game_info['win_count'] / game_info['total_count'], 2) * 100, "% 找到的雷的数目为：",
          game_info['total_flag_count'], "随机点击的次数为：", game_info['guess_count'])


def is_end(game_info, board):
    # 判断是否游戏结束
    # game_info = {'total_count': 0, 'defeat_count': 0, 'win_count': 0,
    #              'total_flag_count': 0, 'guess_count': 0, 'DEFEAT': False}
    game_info['total_flag_count'] = np.sum(board == 8)  # 更新旗的数目
    if MINE in board or RED_MINE in board:
        defeat_game(game_info)
        return True
    if game_info['total_flag_count'] == MAX_FLAG_COUNT and NONE_DETECTED not in board:
        win_game(game_info)
        return True
    return False




