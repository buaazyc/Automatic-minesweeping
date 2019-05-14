from constant import *


def get_surround(board, left_distance, top_distance):
    # 获得该位置周围的所有数字信息，主要考虑边界问题
    # nums中每一个元素[0]表示具体值，[1]表示i，top偏移，[2]表示j，left偏移
    cur_number = board[top_distance][left_distance]
    nums = []
    i = top_distance
    j = left_distance
    if (i == 0 or i == BOARD_HEIGHT - 1) or (j == 0 or j == BOARD_LENGTH - 1):
        # 在边界
        if i == 0 and j == 0:
            # 左上角
            nums.append((board[i + 1][j], i + 1, j))
            nums.append((board[i + 1][j + 1], i + 1, j + 1))
            nums.append((board[i][j + 1], i, j + 1))
        elif i == 0 and j == BOARD_LENGTH - 1:
            # 右上角
            nums.append((board[i][j - 1], i, j - 1))
            nums.append((board[i + 1][j], i + 1, j))
            nums.append((board[i + 1][j - 1], i + 1, j - 1))
        elif i == BOARD_HEIGHT - 1 and j == 0:
            # 左下角
            nums.append((board[i - 1][j + 1], i - 1, j + 1))
            nums.append((board[i - 1][j], i - 1, j))
            nums.append((board[i][j + 1], i, j + 1))
        elif i == BOARD_HEIGHT - 1 and j == BOARD_LENGTH - 1:
            # 右下角
            nums.append((board[i - 1][j - 1], i - 1, j - 1))
            nums.append((board[i][j - 1], i, j - 1))
            nums.append((board[i - 1][j], i - 1, j))
        else:
            if i == 0:
                # 在上边界
                nums.append((board[i][j - 1], i, j - 1))
                nums.append((board[i + 1][j - 1], i + 1, j - 1))
                nums.append((board[i + 1][j], i + 1, j))
                nums.append((board[i][j + 1], i, j + 1))
                nums.append((board[i + 1][j + 1], i + 1, j + 1))
            if i == BOARD_HEIGHT - 1:
                # 在下边界
                nums.append((board[i - 1][j - 1], i - 1, j - 1))
                nums.append((board[i][j - 1], i, j - 1))
                nums.append((board[i - 1][j], i - 1, j))
                nums.append((board[i - 1][j + 1], i - 1, j + 1))
                nums.append((board[i][j + 1], i, j + 1))
            if j == 0:
                # 在左边界
                nums.append((board[i - 1][j], i - 1, j))
                nums.append((board[i + 1][j], i + 1, j))
                nums.append((board[i - 1][j + 1], i - 1, j + 1))
                nums.append((board[i][j + 1], i, j + 1))
                nums.append((board[i + 1][j + 1], i + 1, j + 1))
            if j == BOARD_LENGTH - 1:
                # 在右边界
                nums.append((board[i - 1][j - 1], i - 1, j - 1))
                nums.append((board[i][j - 1], i, j - 1))
                nums.append((board[i + 1][j - 1], i + 1, j - 1))
                nums.append((board[i - 1][j], i - 1, j))
                nums.append((board[i + 1][j], i + 1, j))
    else:
        # 不在边界
        nums.append((board[i - 1][j - 1], i - 1, j - 1))
        nums.append((board[i][j - 1], i, j - 1))
        nums.append((board[i + 1][j - 1], i + 1, j - 1))
        nums.append((board[i - 1][j], i - 1, j))
        nums.append((board[i + 1][j], i + 1, j))
        nums.append((board[i - 1][j + 1], i - 1, j + 1))
        nums.append((board[i][j + 1], i, j + 1))
        nums.append((board[i + 1][j + 1], i + 1, j + 1))
    return nums, cur_number


def get_surround_detail(nums):
    # none_detected_count, flag_count, number_count, null_count
    flag_count = 0
    none_detected_count = 0
    null_count = 0
    number_count = 0
    for num in nums:
        # nums中每一个元素[0]表示具体值，[1]表示i，top偏移，[2]表示j，left偏移
        assert len(num) == 3
        if num[0] == NONE_DETECTED:
            none_detected_count += 1
        elif num[0] == FLAG:
            flag_count += 1
        elif num[0] == NULL:
            null_count += 1
        elif 1 <= num[0] <= 7:
            number_count += 1
    return none_detected_count, flag_count, number_count, null_count
