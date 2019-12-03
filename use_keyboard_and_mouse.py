"""
    对GameWindow进行二次封装，增加键盘和鼠标操作
"""

from window import GameWindow
from win32api import SetCursorPos, mouse_event, keybd_event
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, KEYEVENTF_KEYUP
from PIL import ImageGrab  # pip install pillow, 如果下载速度慢可以去pypi.org下载whl文件
from numpy import array  # pip install numpy, 如果下载速度慢可以去pypi.org下载whl文件
from numpy import zeros, sum, int


class OperateWindow(object):
    def __init__(self):
        self.window = GameWindow()
        self.img = None
        self.info_to_int = {
            'flag': 10,
            'null': 11,
            'unknown': 12,
            'mine': 13,
            'red_mine': 14
        }
        self.int_to_info = dict(zip(self.info_to_int.values(), self.info_to_int.keys()))
        self.chessboard = None

        self.update_chessboard()

    # 单击鼠标左键
    # left_offset和top_offset表示
    # 从左往右第left_offset个，从上往下第top_offset个格子
    # 索引从0开始
    def left_click(self, left_offset, top_offset):
        pos = self.window.get_box(left_offset, top_offset)
        SetCursorPos(pos)
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    # 单击鼠标右键
    # left_offset和top_offset表示
    # 从左往右第left_offset个，从上往下第top_offset个格子
    # 索引从0开始
    def right_click(self, left_offset, top_offset):
        pos = self.window.get_box(left_offset, top_offset)
        SetCursorPos(pos)
        mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    # 鼠标左右键同时按下
    # left_offset和top_offset表示
    # 从左往右第left_offset个，从上往下第top_offset个格子
    # 索引从0开始
    def left_and_right_click(self, left_offset, top_offset):
        pos = self.window.get_box(left_offset, top_offset)
        SetCursorPos(pos)
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    # 按下键盘F2
    def f2(self):
        key_f2 = 113  # f2对应的键盘输入值
        keybd_event(key_f2, 0, 0, 0)
        keybd_event(key_f2, 0, KEYEVENTF_KEYUP, 0)

    # 截图
    def get_img(self):
        self.img = array(ImageGrab.grab((self.window.get_side())))

    # 棋盘
    def update_chessboard(self):
        self.get_img()
        self.chessboard = img_to_chessboard(self.img,
                                            self.window.length,
                                            self.window.height,
                                            self.window.pixel_size,
                                            self.info_to_int)


def img_to_chessboard(img, length, height, pixel_size, info_to_int):
    """
        根据像素信息，将图片转换为棋盘信息
        主要对比的方法是对每个块内所有像素值求和
        恰好该值是独一无二的
        因此可以用来表示对应的块
    """
    assert len(img.shape) == 3
    assert img.shape[0] == height * pixel_size
    assert img.shape[1] == length * pixel_size
    assert img.shape[2] == 3

    map = {
        141504: info_to_int['null'],
        129165: info_to_int['flag'],
        147294: info_to_int['unknown'],
        97908: info_to_int['mine'],
        51684: info_to_int['red_mine'],
        128664: 1,
        112384: 2,
        121602: 3,
        116416: 4,
        110144: 5,
        118464: 6,
        116160: 7,
        126912: 8
    }

    # d = set()

    chessboard = zeros((height, length), dtype=int)  # 初始化棋盘
    for i in range(height):
        for j in range(length):
            # 遍历chessboard每个位置
            # 截取对应img位置上的小图片区域
            img_piece = img[i * pixel_size: (i + 1) * pixel_size,
                        j * pixel_size: (j + 1) * pixel_size, :]
            assert img_piece.shape == (pixel_size, pixel_size, 3)

            sum_val = sum(img_piece)
            if sum_val in map.keys():
                chessboard[i][j] = map[sum_val]
            else:
                # print("颜色判断错误", sum_val)
                chessboard[i][j] = sum_val
            # d.add(sum_val)

    # print(chessboard)
    # print(len(d))
    return chessboard


if __name__ == '__main__':
    op = OperateWindow()

