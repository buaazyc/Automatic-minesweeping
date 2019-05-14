#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 作者: 张艺川
# 时间：2019/3/24
# 功能：实现经典版扫雷的自动实现脚本，只实现了高级中级低级，不包含自定义
import numpy as np
from constant import *
from begin import begin, focus
from mine_analysis import mine_analysis


if __name__ == '__main__':
    sum_board = np.zeros((BOARD_HEIGHT, BOARD_LENGTH), dtype=int)
    title_name = "扫雷"
    hwnd = win32gui.FindWindow(None, title_name)  # 获得窗口
    assert hwnd
    # game_info保存游戏基本信息
    # 内容分别是总局数，失败的次数，成功的次数，当前游戏插旗的数目，随机点击的次数，是否失败
    game_info = {'total_count': 0, 'defeat_count': 0, 'win_count': 0,
                 'total_flag_count': 0, 'guess_count': 0, 'DEFEAT': False}
    focus(hwnd)  # 刚开始点击扫雷屏幕中间
    begin(hwnd, game_info)
    while game_info['DEFEAT']:
        # 如果输了就重新开
        begin(hwnd, game_info)

    # 循环多次，保存雷的分布结果
    # for i in range(100):
    #     board = begin(hwnd, game_info)
    #     mine_info = np.where(((board == FLAG) | (board == MINE) | (board == RED_MINE)), 1, 0)
    #     sum_board += mine_info
    # mine_analysis(sum_board, game_info)








