"""
    定义每个格子及其周围8个格子的类
"""


class BoxWithSurround(object):
    def __init__(self, chessboard, top_offset, left_offset, info_to_int, int_to_info):
        self.val = chessboard[top_offset][left_offset]
        self.chessboard = chessboard
        self.top_offset = top_offset
        self.left_offset = left_offset
        self.length = chessboard.shape[1]
        self.height = chessboard.shape[0]
        self.info_to_int = info_to_int
        self.int_to_info = int_to_info

        # 假设元素在电脑小键盘5的位置
        # 其相邻值就是对应的12346789的位置
        self.nearby = {
            '_1': self.is_out(-1, 1),
            '_2': self.is_out(0, 1),
            '_3': self.is_out(1, 1),
            '_4': self.is_out(-1, 0),
            '_6': self.is_out(1, 0),
            '_7': self.is_out(-1, -1),
            '_8': self.is_out(0, -1),
            '_9': self.is_out(1, -1)
        }

        # 统计nearby的分布情况
        self.distribution = {
            'flag': [],
            'unknown': [],
            'null': [],
            'digit': [],
            'mine': [],
            'red_mine': []
        }
        self.set_distribution()

    # 判断是否出界
    def is_out(self, top_offset, left_offset):
        x = self.top_offset + top_offset
        y = self.left_offset + left_offset
        # 如果超出边界就是视为null
        if x < 0 or x >= self.height or y < 0 or y >= self.length:
            return self.info_to_int['null']
        else:
            return self.chessboard[x][y]

    # 统计每个格子四周的分布情况
    def set_distribution(self):
        for key_val in self.nearby.items():
            val_int = key_val[1]
            # 如果是flag null或者unknown
            if self.int_to_info.get(val_int, None):
                val_info = self.int_to_info[val_int]
                self.distribution[val_info].append(key_val[0])
            # 如果是数字
            else:
                self.distribution['digit'].append(key_val[0])
        # 统计总长度为8
        assert sum([len(key_val[1]) for key_val in self.distribution.items()]) == 8
        # print(self.distribution)

    # pos 2 offset
    def pos_to_offset(self, pos):
        dic = {
            # top_offset, left_offset
            '_1': (-1, 1),
            '_2': (0, 1),
            '_3': (1, 1),
            '_4': (-1, 0),
            '_6': (1, 0),
            '_7': (-1, -1),
            '_8': (0, -1),
            '_9': (1, -1)
        }
        assert pos in dic.keys()
        top_offset = self.top_offset + dic[pos][0]
        left_offset = self.left_offset + dic[pos][1]
        return top_offset, left_offset

    def get_surround(self):
        res = list()
        for pos in self.nearby.keys():
            if self.nearby[pos] in [self.info_to_int['flag'], self.info_to_int['unknown']]:
                top_offset, left_offset = self.pos_to_offset(pos)
                if 0 <= top_offset < self.height and 0 <= left_offset < self.length:
                    res.append((top_offset, left_offset))
        # print("get_surround" + str(res))
        return res
