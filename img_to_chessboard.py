"""
    根据像素信息，将图片转换为棋盘信息
    主要对比的方法是对每个块内所有像素值求和后取平均
    恰好该均值是独一无二的
    因此可以用来表示对应的块
"""
import numpy as np

def img_to_chessboard(img, length, height, pixel_size, info_to_int):
    assert len(img.shape) == 3
    assert img.shape[0] == height * pixel_size
    assert img.shape[1] == length * pixel_size
    assert img.shape[2] == 3

    value_to_info = {
        168.18: info_to_int['flag'],  # 红旗
        184.25: info_to_int['null'],  # 空
        191.79: info_to_int['unknown'],  # 未检测
        127.48: info_to_int['mine'],  # 黑雷
        67.30: info_to_int['red_mine'],  # 红雷
        167.53: 1,
        146.33: 2,
        158.34: 3,
        151.58: 4,
        143.42: 5,
        154.25: 6,
        151.25: 7,
        165.25: 8
    }

    chessboard = np.zeros((height, length), dtype=np.int)  # 初始化棋盘
    for i in range(height):
        for j in range(length):
            # 遍历chessboard每个位置
            # 截取对应img位置上的小图片区域
            img_piece = img[i * pixel_size: (i + 1) * pixel_size,
                        j * pixel_size: (j + 1) * pixel_size, :]
            assert img_piece.shape == (pixel_size, pixel_size, 3)
            # 对小图片像素值取均值
            avg_val = np.sum(img_piece) / (pixel_size * pixel_size * 3)
            # 查字典后得对应内容
            avg_val = round(avg_val, 2)
            chessboard[i][j] = value_to_info[avg_val]

    # print(chessboard)
    return chessboard
