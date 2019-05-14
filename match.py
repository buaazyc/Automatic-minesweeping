from constant import *


def get_corresponding_content(img, i, j):
    # 根据每一个块特定点的像素值不同，进行匹配
    # 将i j转化为对应具体的像素位置
    i = int(i * PIXEL_SIZE)
    j = int(j * PIXEL_SIZE)

    for index, color in enumerate(rgb):
        match_point = list(img[i + 3, j + 9, :])  # 对比每块相对于其左上角偏移（3,9）位置的像素点的RGB值
        assert len(match_point) == 3  # RGB值，例如[255, 255, 255]

        if color == match_point:
            # 当为数字1-6的时候,匹配正确，除了3以为用数字直接代替
            if index + 1 <= 6:
                if list(img[i + 10, j + 10, :]) == [0, 0, 0] and index + 1 == 3:
                    # 红雷
                    return RED_MINE
                else:
                    return index + 1
            # 当为数字7的时候，显示的是8
            if index + 1 == 8:
                return 7
            # 当显示的是数字7时候，为 none，flag，null，雷
            if index + 1 == 7:
                if list(img[i + 6, j + 6, :]) == [255, 0, 0]:
                    # flag
                    return FLAG
                if list(img[i + 1, j + 1, :]) == [255, 255, 255]:
                    # none
                    return NONE_DETECTED
                if list(img[i + 10, j + 10, :]) == [0, 0, 0]:
                    # 黑雷
                    return MINE
                if list(img[i + 1, j + 1, :]) == [192, 192, 192]:
                    # null
                    return NULL
                else:
                    print("get_rgb_match失败")
                    return OTHER
