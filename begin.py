from constant import *
from choose_next_click import choose_next_click
from basic_operation import left_click, remake
from game_end import is_end
import numpy as np
from choose_next_click import random_click


def begin(hwnd, game_info):
    # game_info = {'total_count': 0, 'defeat_count': 0, 'win_count': 0,
    #              'total_flag_count': 0, 'guess_count': 0, 'DEFEAT': False}
    # 初始化游戏信息
    game_info['total_count'] += 1
    game_info['total_flag_count'] = 0
    game_info['guess_count'] = 0
    game_info['DEFEAT'] = False

    # board矩阵用于保存扫雷每个点的信息,初始化为
    board = np.zeros((BOARD_HEIGHT, BOARD_LENGTH), dtype=int)
    board = np.full(board.shape, NONE_DETECTED)
    # 重新打开游戏
    remake()
    random_click(board, hwnd, game_info)  # 随机点
    # 每次都以点击中心作为开始
    # left_click(hwnd, BOARD_LENGTH // 2, BOARD_HEIGHT // 2)
    # 如果游戏没有结束就不断寻找下一个点击点
    while not is_end(game_info, board):
        choose_next_click(board, hwnd, game_info)
    return board


def focus(hwnd):
    # 第一局需要先侧换到扫雷界面上，点击界面
    left_click(hwnd, BOARD_LENGTH // 2, BOARD_HEIGHT // 2)
