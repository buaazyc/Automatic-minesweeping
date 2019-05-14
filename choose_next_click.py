# 寻找下一个点击的位置
from constant import *
from random import shuffle
from get_surround import get_surround_detail, get_surround
from basic_operation import goon, make_flag, open_surround


def choose_next_click(board, hwnd, game_info):
    # 首先基本判断
    if NONE_DETECTED in board:
        find_best = False
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_LENGTH):
                # 遍历整个board
                if 1 <= board[i][j] <= 7:
                    # 找到一个数字
                    # 得到它周围数字信息
                    nums, cur_number = get_surround(board, j, i)
                    none_detected_count, flag_count, number_count, null_count = get_surround_detail(nums)
                    # nums中每一个元素[0]表示具体值，[1]表示i，top偏移，[2]表示j，left偏移

                    if none_detected_count == 0:
                        # 该数字周围没有未检测的方块，跳到下一个方块
                        continue
                    elif flag_count == cur_number:
                        # 该数字等于周围旗数，则通过双击数字打开周围没有检测的方块
                        open_surround(hwnd, j, i, board)
                        find_best = True
                    elif flag_count + none_detected_count == cur_number:
                        # 该数字等于周围旗+未检测数目,则将未检测方块插旗
                        for num in nums:
                            if num[0] == NONE_DETECTED:
                                make_flag(num[2], num[1], board, hwnd, game_info)
                                find_best = True
        if not find_best:
            # 遍历所有board之后没有找到最优位置，则启动高级检测
            advanced(board, hwnd, game_info)


def advanced(board, hwnd, game_info):
    # 根据两个相邻数字的情况去判断
    find_best = False
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            # 遍历整个board
            if 1 <= board[i][j] <= 7:
                cur_num = board[i][j]  # 是数字
                cur_nums_copy = get_surround(board, j, i)[0]  # 得到周围数字信息

                for num in cur_nums_copy:  # 遍历周围数字
                    assert len(num) == 3
                    # nums中每一个元素[0]表示具体值，[1]表示i，top偏移，[2]表示j，left偏移
                    if 1 <= num[0] <= 7 and (num[1] == i or num[2] == j):
                        # 如果在有两个相邻的数字
                        neighbor_nums, neighbor_num = get_surround(board, num[2], num[1])  # 第二个数字周围信息

                        cur_nums = cur_nums_copy.copy()
                        # cur_nums表示一个数字周围的内容
                        # neighbor_nums表示相邻数字周围的内容
                        # shared_nums表示共有的
                        shared_nums = list(set(cur_nums) & set(neighbor_nums))
                        cur_nums = list(set(cur_nums) - set(shared_nums))
                        neighbor_nums = list(set(neighbor_nums) - set(shared_nums))

                        # 两个数字相互删除对方
                        if num in cur_nums:
                            cur_nums.remove(num)
                        if (cur_num, i, j) in neighbor_nums:
                            neighbor_nums.remove((cur_num, i, j))

                        # [0]none_detected_count, [1]flag_count, [2]number_count, [3]null_count
                        cur_sur_detail = get_surround_detail(cur_nums)
                        neighbor_sur_detail = get_surround_detail(neighbor_nums)
                        shared_sur_detail = get_surround_detail(shared_nums)

                        cur_all_mine = cur_num - cur_sur_detail[1] - shared_sur_detail[1]  # 当前数字的雷数目
                        share_at_least_mine = cur_all_mine - cur_sur_detail[0]  # 公共区域雷的最少数目
                        share_most_mine = min(cur_all_mine, 2)  # 公告区域雷最多的数目

                        neighbor_all_mine = neighbor_num - neighbor_sur_detail[1] - shared_sur_detail[1]  # 邻居雷数
                        share_at_least_mine_n = neighbor_all_mine - neighbor_sur_detail[0]  # 根据邻居计算的最少公共雷

                        if share_most_mine == share_at_least_mine_n and shared_sur_detail[0] == 2:
                            # 如果当前数字公共最多的雷，等于，邻居在公共区域雷最少数目
                            # 则邻居未检测区域为雷
                            for have_mine in neighbor_nums:
                                if have_mine[0] == NONE_DETECTED:
                                    make_flag(have_mine[2], have_mine[1], board, hwnd, game_info)
                                    find_best = True

                        if shared_sur_detail[0] == 2 and share_at_least_mine == 1 and neighbor_all_mine == 1:
                            # 如果当前数字计算的公共至少的雷数目，等于，邻居所有的雷数目
                            # 则邻居未检测区域为旗
                            for no_mine in neighbor_nums:
                                if no_mine[0] == NONE_DETECTED:
                                    goon(no_mine[2], no_mine[1], board, hwnd)
                                    find_best = True
    if not find_best:
        random_click(board, hwnd, game_info)


def random_click(board, hwnd, game_info):
    # if game_info['total_flag_count'] == MAX_FLAG_COUNT:
    #     last_click(board, hwnd)
    none_detected = []
    max_count = 0

    # 循环找到周围最大未检测数
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            if board[i][j] == NONE_DETECTED:
                none_detected_count = get_surround_detail(get_surround(board, j, i)[0])[0]
                if none_detected_count > max_count:
                    max_count = none_detected_count
    # 循环找到具有这些最大未检测数的方块
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            if board[i][j] == NONE_DETECTED:
                none_detected_count = get_surround_detail(get_surround(board, j, i)[0])[0]
                if none_detected_count == max_count:
                    none_detected.append((i, j))

    game_info['guess_count'] += 1  # 随机点击的次数 +1
    shuffle(none_detected)  # 打乱顺序
    next_click_point = none_detected[0]
    goon(next_click_point[1], next_click_point[0], board, hwnd)
