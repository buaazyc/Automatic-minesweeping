"""
    封装每局游戏的基本操作
"""
from use_keyboard_and_mouse import OperateWindow
from numpy import sum


class BasicOperation(object):
    def __init__(self):
        self.op = OperateWindow()
        self.length = self.op.chessboard.shape[1]
        self.height = self.op.chessboard.shape[0]
        self.find_mines = sum(self.op.chessboard == self.op.info_to_int['flag'])
        self.unknown_boxes = sum(self.op.chessboard == self.op.info_to_int['unknown'])
    
    # 更新棋盘chessboard
    def refresh(self):
        self.op.update_chessboard()
        self.find_mines = sum(self.op.chessboard == self.op.info_to_int['flag'])
        self.unknown_boxes = sum(self.op.chessboard == self.op.info_to_int['unknown'])
        
    # 标红旗
    def make_flag(self, left_offset, top_offset):
        assert self.op.chessboard[top_offset][left_offset] == self.op.info_to_int['unknown']
        self.op.right_click(left_offset, top_offset)
        self.op.chessboard[top_offset][left_offset] = self.op.info_to_int['flag']
    
    # 点击区域
    def go(self, left_offset, top_offset):
        assert self.op.chessboard[top_offset][left_offset] == self.op.info_to_int['unknown']
        self.op.left_click(left_offset, top_offset)
        self.refresh()

    # 点击中央
    def center(self):
        # print("center:({},{})".format(self.length // 2, self.height // 2))
        self.go(left_offset=self.length // 2, top_offset=self.height // 2)

    # 重开
    def remake(self):
        self.op.f2()
        # 第一步点击屏幕中央
        self.refresh()
        self.center()
    
    # 同时按下左右键打开一片区域
    def open_surround(self, left_offset, top_offset):
        self.op.left_and_right_click(left_offset, top_offset)
        self.refresh()


if __name__ == '__main__':
    basic_op = BasicOperation()
