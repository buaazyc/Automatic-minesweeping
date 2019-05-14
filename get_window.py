import win32gui
PIXEL_SIZE = 16  # ，每个格子像素大小
HIGH_LEVEL = 3  # 三个等级
MIDDLE_LEVEL = 2
PRIMARY_LEVEL = 1


def get_rim(hwnd):
    # 获得出去边框之外的界面的长宽位置
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 窗口大小
    left = left + 15
    right = right - 11
    bottom = bottom - 11
    top = bottom - PIXEL_SIZE * get_window_height_and_length(hwnd)[0]
    assert (right - left) / PIXEL_SIZE == get_window_height_and_length(hwnd)[1]  # 长度length
    assert (bottom - top) / PIXEL_SIZE == get_window_height_and_length(hwnd)[0]  # 高度height
    return left, top, right, bottom


def get_ranking_level(hwnd):
    # 根据长宽尺寸判断高级，中级，低级
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 窗口大小
    left = left + 15
    right = right - 11
    length = (right - left) / PIXEL_SIZE
    if length == 30:
        return HIGH_LEVEL  # 高级
    elif length == 16:
        return MIDDLE_LEVEL
    elif length == 9:
        return PRIMARY_LEVEL
    else:
        print("根据尺寸计算扫雷等级错误")


def get_window_height_and_length(hwnd):
    # 根据等级返回长宽格子数目
    ranking_level = get_ranking_level(hwnd)
    if ranking_level == HIGH_LEVEL:
        return 16, 30
    elif ranking_level == MIDDLE_LEVEL:
        return 16, 16
    else:
        return 9, 9


def get_max_mines(hwnd):
    # 根据等级得到雷数目
    ranking_level = get_ranking_level(hwnd)
    if ranking_level == HIGH_LEVEL:
        return 99
    elif ranking_level == MIDDLE_LEVEL:
        return 40
    else:
        return 10
