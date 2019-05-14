# 用于进行鼠标键盘截图等与计算机进行的底层操作
import win32con
import win32api
from PIL import ImageGrab
from constant import *
from get_window import get_rim
import numpy as np


def left_click(hwnd, left_distance, top_distance):
    # 单击左键一次
    left, top = get_left_top(hwnd)
    win32api.SetCursorPos([left + left_distance * PIXEL_SIZE + PIXEL_SIZE // 2,
                           top + top_distance * PIXEL_SIZE + PIXEL_SIZE // 2])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def right_click(hwnd, left_distance, top_distance):
    # 单击右键一次
    left, top = get_left_top(hwnd)
    win32api.SetCursorPos([left + left_distance * PIXEL_SIZE + PIXEL_SIZE // 2,
                           top + top_distance * PIXEL_SIZE + PIXEL_SIZE // 2])
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def double_click(hwnd, left_distance, top_distance):
    # 左右键同时按下
    left, top = get_left_top(hwnd)
    win32api.SetCursorPos([left + left_distance * PIXEL_SIZE + PIXEL_SIZE // 2,
                           top + top_distance * PIXEL_SIZE + PIXEL_SIZE // 2])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def remake_f2():
    key_f2 = 113  # F2对应的键盘输入值
    win32api.keybd_event(key_f2, 0, 0, 0)
    win32api.keybd_event(key_f2, 0, win32con.KEYEVENTF_KEYUP, 0)


def get_left_top(hwnd):
    # 得到边框的左和上
    return get_rim(hwnd)[0:2]


def get_image(hwnd):
    # 得到界面的截图
    left, top, right, bottom = get_rim(hwnd)
    img = ImageGrab.grab((left, top, right, bottom))  # 截图
    img = np.array(img)  # 转化为一个三维数组，第三维表示通道数
    assert img.shape == (BOARD_HEIGHT * PIXEL_SIZE, BOARD_LENGTH * PIXEL_SIZE, 3)
    return img
