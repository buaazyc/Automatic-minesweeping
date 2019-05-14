from get_window import PIXEL_SIZE, get_window_height_and_length, get_max_mines
import win32gui
BOARD_HEIGHT, BOARD_LENGTH = get_window_height_and_length(win32gui.FindWindow(None, "扫雷"))  # 长宽的格子数目
PIXEL_SIZE = PIXEL_SIZE  # 每个格子的像素大小
FLAG = 8
NULL = 9
MINE = 10
RED_MINE = 11
NONE_DETECTED = 12
OTHER = 8888
MAX_FLAG_COUNT = get_max_mines(win32gui.FindWindow(None, "扫雷"))  # 雷的数目

rgb = [[0, 0, 255], [0, 128, 0], [255, 0, 0], [0, 0, 128], [128, 0, 0], [0, 128, 128],
       [192, 192, 192], [0, 0, 0], [255, 255, 255]]
