"""
扫雷游戏窗口
"""
# pip install pywin32,如果下载速度慢可以去pypi.org下载whl文件,务必安装223版本，其他版本不行
from win32gui import FindWindow, GetWindowRect, SetForegroundWindow, SendMessage
from win32con import WM_SYSCOMMAND, SC_RESTORE


class GameWindow(object):
    def __init__(self):
        self.hwnd = FindWindow(None, "扫雷")  # 获取扫雷游戏窗口的句柄
        assert self.hwnd, "请先打开扫雷，再运行该脚本程序"
        SendMessage(self.hwnd, WM_SYSCOMMAND, SC_RESTORE, 0)  # 还原最小化
        SetForegroundWindow(self.hwnd)  # 窗口置顶

        self.pixel_size = 16  # 每个格子的大小固定，为16个像素
        self.left, self.top, self.right, self.bottom = GetWindowRect(self.hwnd)  # 获取窗口坐标
        self.rank = None  # 扫雷游戏的等级，分为：高级、中级、初级，不包含自定义模式
        self.max_mines = 0  # 扫雷游戏的所有雷的数目

        # 去除窗口边框，只保留所有格子
        self.left = self.left + 15  # 左边框15个像素宽
        self.right = self.right - 11  # 右边框11个像素宽
        self.bottom = self.bottom - 11  # 下边框11个像素宽
        self.top = self.top + 101  # 尚边框101个像素宽

        # 获得游戏横向和纵向的格子数目
        self.height = int((self.bottom - self.top) / self.pixel_size)  # 扫雷游戏的纵向格子数目
        assert self.height in [16, 16, 9]
        self.length = int((self.right - self.left) / self.pixel_size)  # 扫雷游戏的横向格子数目
        assert self.length in [30, 16, 9]

        # 获取游戏难度级别
        self.get_rank()
        self.get_max_mines()

    def get_side(self):
        return self.left, self.top, self.right, self.bottom

    def get_rank(self):
        length_to_rank = {30: '高级', 16: '中级', 9: '初级'}
        self.rank = length_to_rank[self.length]

    def get_max_mines(self):
        rank_to_max_mines = {'高级': 99, '中级': 40, '初级': 10}
        self.max_mines = rank_to_max_mines[self.rank]

    def get_box(self, left_offset, top_offset):
        # 根据角标返回对应格子的屏幕像素坐标
        # left_offset和top_offset表示
        # 从左往右第left_offset个，从上往下第top_offset个格子
        # 索引从0开始
        assert 0 <= left_offset < self.length
        assert 0 <= top_offset < self.height
        left_pos = self.left + left_offset * self.pixel_size + self.pixel_size // 2
        top_pos = self.top + top_offset * self.pixel_size + self.pixel_size // 2
        return left_pos, top_pos

    def get_center(self):
        # 获取游戏正中心格子的屏幕像素坐标
        left_offset = self.length // 2
        top_offset = self.height // 2
        center = self.get_box(left_offset, top_offset)
        return center


if __name__ == '__main__':
    win = GameWindow()


