"""
    定义每局游戏
"""
from basic_operation import BasicOperation
from surround import BoxWithSurround
from random import shuffle


class Game(object):
    def __init__(self):
        self.basic_op = BasicOperation()
        self.basic_op.refresh()
        self.info_to_int = self.basic_op.op.info_to_int
        self.int_to_info = self.basic_op.op.int_to_info
        self.length = self.basic_op.op.window.length
        self.height = self.basic_op.op.window.height
        self.max_mines = self.basic_op.op.window.max_mines

    # 运行
    def run(self):
        # 如果程序运行时已经输了或者已经赢了就重开
        if self.game_over() or self.win():
            self.basic_op.remake()

        # 如果新开的一把，就从中间开始点
        if self.new():
            self.basic_op.center()

        # 否则就继续游戏
        while not self.game_over() and not self.win():
            self.choose_next_click()

        if self.game_over():
            print('Game Over')
        if self.win():
            print('Win')

    # 判断是否游戏失败
    def game_over(self):
        return self.info_to_int['mine'] in self.basic_op.op.chessboard

    # 判断是否胜利
    def win(self):
        find_all = self.basic_op.find_mines == self.max_mines

        # 解决旗子插完但是还有未点击格子的问题
        if find_all:
            for top_offset in range(self.height):
                for left_offset in range(self.length):
                    if self.basic_op.op.chessboard[top_offset][left_offset] == self.info_to_int['unknown']:
                        self.basic_op.go(left_offset, top_offset)
        return find_all

    # 判断是否是新的一盘
    def new(self):
        return self.basic_op.unknown_boxes == self.length * self.height

    # 判断不出有把握的，就点第一个unknown
    def random(self):
        unknown_list = []
        for top_offset in range(self.height):
            for left_offset in range(self.length):
                if self.basic_op.op.chessboard[top_offset][left_offset] == self.info_to_int['unknown']:
                    unknown_list.append((left_offset, top_offset))

        shuffle(unknown_list)
        left_offset, top_offset = unknown_list[0]
        self.basic_op.go(left_offset, top_offset)
        return


    # 根据列表中的坐标，统计旗的数量和雷的数量
    def count_list(self, pos_list):
        map = {
            'flag': 0,
            'unknown': 0
        }
        for pos in pos_list:
            val = self.basic_op.op.chessboard[pos[0]][pos[1]]
            if val > 8:
                var = self.int_to_info[val]
                if var in map.keys():
                    map[var] += 1
        return map

    # 选择下一次点击的位置，决策部分
    def choose_next_click(self):
        # 首先遍历所有格子
        for top_offset in range(self.height):
            for left_offset in range(self.length):
                # 定义每个格子
                box = BoxWithSurround(self.basic_op.op.chessboard,
                                      top_offset,
                                      left_offset,
                                      self.info_to_int,
                                      self.int_to_info)

                # 只处理数字格子，并且周围有unknown格子
                if box.val <= 8 and len(box.distribution['unknown']) != 0:
                    # 如果已经插旗数目等于当前格子的数字，则周围其他格子都不是雷
                    if len(box.distribution['flag']) == box.val:
                        self.basic_op.open_surround(left_offset, top_offset)
                        return

                    # 如果插旗数+未检测数等于当前数字，则未检测全是雷
                    elif len(box.distribution['flag']) + len(box.distribution['unknown']) == box.val:
                        for pos in box.distribution['unknown']:
                            t, l = box.pos_to_offset(pos)
                            self.basic_op.make_flag(left_offset=l, top_offset=t)
                            return

                    # 如果还不行，就要根据相邻数字进行组合推导
                    elif len(box.distribution['digit']) > 0:
                        for pos in box.distribution['digit']:
                            t, l = box.pos_to_offset(pos)
                            if t == top_offset or l == left_offset:
                                # 找到两个相邻的数字
                                neighbor = BoxWithSurround(self.basic_op.op.chessboard,
                                                           top_offset=t,
                                                           left_offset=l,
                                                           info_to_int=self.info_to_int,
                                                           int_to_info=self.int_to_info)

                                # 分别获得两个格子周围的有效格子
                                # 旗或者未检测
                                # flag 或者 unknown
                                box_surround = box.get_surround()
                                neighbor_surround = neighbor.get_surround()

                                # 共享的格子share
                                share = list(set(box_surround) & set(neighbor_surround))
                                # 各自双方
                                selves = [(t, l), (top_offset, left_offset)]

                                # 删除掉共享和各自双方后，剩下的私有的格子
                                box_surround = list(set(box_surround) - set(share) - set(selves))
                                neighbor_surround = list(set(neighbor_surround) - set(share) - set(selves))

                                # 统计
                                # {'flag': 0, 'unknown': 2}
                                box_map = self.count_list(box_surround)
                                neighbor_map = self.count_list(neighbor_surround)
                                share_map = self.count_list(share)

                                # 如果box在公共最多的雷数 == neighbor在公共最少的雷数
                                if min(box.val - box_map['flag'] - share_map['flag'], 2) == \
                                    neighbor.val - neighbor_map['flag'] - neighbor_map['unknown'] - share_map['flag'] and \
                                        share_map['unknown'] == 2:

                                        for pos in neighbor_surround:
                                            if self.basic_op.op.chessboard[pos[0]][pos[1]] == self.info_to_int['unknown']:
                                                self.basic_op.make_flag(left_offset=pos[1], top_offset=pos[0])
                                                return

                                # 如果box在公共最少的雷 == neighbor所有的雷
                                if share_map['unknown'] == 2 and \
                                        box.val - box_map['unknown'] - box_map['flag'] - share_map['flag'] == 1 and \
                                        neighbor.val - neighbor_map['flag'] - share_map['flag'] == 1:

                                    for pos in neighbor_surround:
                                        if self.basic_op.op.chessboard[pos[0]][pos[1]] == self.info_to_int['unknown']:
                                            self.basic_op.go(left_offset=pos[1], top_offset=pos[0])
                                            return

        # 如果没有找到百分百概率，则随机点
        self.random()


if __name__ == '__main__':
    g = Game()
    g.run()
