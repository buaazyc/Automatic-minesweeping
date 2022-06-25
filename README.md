# Automatic-minesweeping（自动扫雷）
Automatic minesweeping for Windows XP classic version minesweeper by Python3.7  
使用Python编写脚本，实现对经典扫雷游戏的程序自动完成游戏

## exe脚本使用方法：
1. 打开扫雷
2. 运行exe脚本程序

## 源码运行方式
```shell
python game.py
```

## My Operating environment：
Windows 10  
Python 3.7  
Windows经典的Minesweeper游戏

## Program requirement： 
Numpy：用于矩阵运算  
pillow：用于截图，根据截图判断每个格子内容  
pywin32：用户获取窗口，使用鼠标键盘
```shell
pip install numpy
pip install pillow
pip install pywin32
```

## 主要思路：  
1. 使用pywin32获取扫雷游戏的窗口，并模拟键盘鼠标操作进行点击和插旗  
2. 利用截图中，各个块像素点的和来区分各个块，比如块“1”的像素点和为128664，块“红旗”的像素点和为129165，从而将图片信息转化为矩阵信息，矩阵对应着游戏中整个棋盘  
3. 遍历矩阵每个元素，根据周边信息去判断什么时候插旗，什么时候点击，什么时候左右键同时  
4. 循环遍历直到游戏失败或者胜利  

## 代码结构：
1. window.py主要定义基础窗口类，用于获得基本的窗口信息  
2. use_keyboard_and_mouse.py顾名思义定义了鼠标和键盘操作类  
3. basic_operation.py封装了之前的类，实现了扫雷的基本操作，比如点击，插旗，重开等  
4. game.py是脚本运行的主逻辑，进行循环遍历判断决策等。  
5. surround.py定义了格子及其周边信息类，用于判断当前局势，方便决策   

## 功能局限：
1. 目前只支持高级、中级、低级三种默认棋盘大小，不知道自定义模式

## 遇到的问题：
1. IndexError: list index out of range
原因：似乎是屏幕分辨率设置了缩进导致，设置为100%即可（win10-右键-显示设置-缩放与布局-100%）
