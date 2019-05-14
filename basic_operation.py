from constant import *
from keyboard_mouse import double_click, get_image, right_click, left_click, remake_f2
from match import get_corresponding_content


def refresh(hwnd, board):
    # 更新board的内容
    img = get_image(hwnd)  # 截图
    # 遍历board每个位置，进行match，判断其具体内容
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            board[i][j] = get_corresponding_content(img, i, j)


def make_flag(left_distance, top_distance, board, hwnd, game_info):
    # 标红旗
    assert board[top_distance][left_distance] == NONE_DETECTED
    # 此处不用refresh，因为插旗不会导致其他位置改变
    right_click(hwnd, left_distance, top_distance)
    board[top_distance][left_distance] = FLAG
    # total_flag_count = game_info[3]
    game_info['total_flag_count'] += 1


def goon(left_distance, top_distance, board, hwnd):
    # 点一个特定的区域
    if board[top_distance][left_distance] == NONE_DETECTED:
        left_click(hwnd, left_distance, top_distance)
        refresh(hwnd, board)


def remake():
    # 通过传入键盘F2，进行扫雷的重开
    remake_f2()


def open_surround(hwnd, j, i, board):
    # 通过双击坐标（i，j）打开其周围的方块，之后，更新board
    double_click(hwnd, j, i)
    refresh(hwnd, board)

