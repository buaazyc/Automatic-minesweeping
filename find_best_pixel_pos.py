# 用于寻找良好区分各个块的像素点，不参与实际运行
import numpy as np
import win32gui
from PIL import ImageGrab
import matplotlib.pyplot as plt


board = np.zeros((16, 30), dtype=int)
title_name = "扫雷"
hwnd = win32gui.FindWindow(None, title_name)  # 获得窗口

left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 窗口大小
left = left + 15
top = top + 101
right = right - 11
bottom = bottom - 11
image = ImageGrab.grab((left, top, right, bottom))
image = np.array(image)

# 更新board的内容
max = 0
max_x, max_y = 0, 0
max_pixel = []
for offset in range(16 * 16):
    pixel_values = []
    i = 0
    offset_x, offset_y = 0, 0
    while i < 256:
        j = 0
        while j < 480:
            offset_x, offset_y = offset // 16, offset % 16
            pixel_value = image[i + offset_x, j + offset_y, :]
            pixel_value = list(pixel_value)
            if pixel_value not in pixel_values:
                pixel_values.append(pixel_value)
            j += 16
        i += 16
    if len(pixel_values) > max:
        max = len(pixel_values)
        max_x, max_y = offset_x, offset_y
        max_pixel = pixel_values
    if len(pixel_values) == 8:
        print((max_x, max_y))
print(max, (max_x, max_y))
print(max_pixel)
# [[0, 0, 0], [192, 192, 192], [0, 128, 0], [255, 0, 0], [0, 0, 255], [0, 0, 128], [128, 0, 0]]
plt.imshow(image)
plt.show()