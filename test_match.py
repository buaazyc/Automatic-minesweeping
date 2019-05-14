# 用于测试读取图片的效果，不参与实际运行
import numpy as np
import win32gui
from PIL import ImageGrab
import matplotlib.pyplot as plt


rgb = [[0, 0, 255], [0, 128, 0], [255, 0, 0], [0, 0, 128], [128, 0, 0], [0, 128, 128],
       [192, 192, 192], [0, 0, 0], [255, 255, 255]]

FLAG = 8
NULL = 9
MINE = 10
RED_MINE = 11
NONE_DETECTED = 12
OTHER = 8888


def get_rgb_match(img, inter_i, inter_j):
    for inter_k in range(9):
        match_point = list(img[inter_i + 3, inter_j + 9, :])
        if rgb[inter_k] == match_point:
            # 当为数字1-6的时候
            if inter_k + 1 <= 6:
                if list(img[inter_i + 10, inter_j + 10, :]) == [0, 0, 0] and inter_k + 1 == 3:
                    # 红雷
                    return RED_MINE
                else:
                    return inter_k + 1
            # 当为数字7的时候
            if inter_k + 1 == 8:
                return 7
            # 当为 none，flag，null，雷的时候
            if inter_k + 1 == 7:
                if list(img[inter_i + 6, inter_j + 6, :]) == [255, 0, 0]:
                    # flag
                    return FLAG
                if list(img[inter_i + 1, inter_j + 1, :]) == [255, 255, 255]:
                    # none
                    return NONE_DETECTED
                if list(img[inter_i + 10, inter_j + 10, :]) == [0, 0, 0]:
                    # 黑雷
                    return MINE
                if list(img[inter_i + 1, inter_j + 1, :]) == [192, 192, 192]:
                    # null
                    return NULL
                else:
                    return OTHER


board = np.zeros((16, 30), dtype=int)
title_name = "扫雷"
hwnd = win32gui.FindWindow(None, title_name)  # 获得窗口

left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 窗口大小
left = left + 15
right = right - 11
bottom = bottom - 11
top = bottom - 256
print(right - left, bottom - top)
image = ImageGrab.grab((left, top, right, bottom))
image = np.array(image)

# 更新board的内容
i, j = 0, 0
while i < 256:
    while j < 480:
        board[i//16][j//16] = get_rgb_match(image, i, j)
        j += 16
    i += 16
    j = 0
print(board)
plt.imshow(image)
plt.show()


