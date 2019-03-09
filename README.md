# FuncPrinter

这是一个简易的函数计算器

main.py --> 程序本体
fpconf.py --> 程序配置文件

### ABOUT 'fpconf':

SCREEN_HEIGHT -> 屏幕高度
SCREEN_WIDTH  -> 屏幕宽度

AXIS_X -> X轴位于屏幕的坐标
AXIS_Y -> Y轴位于屏幕的坐标

DEFAULT_X_AXIS_ZOOM -> X轴的缩放
DEFAULT_Y_AXIS_ZOOM -> Y轴的缩放

DEFAULT_X -> X轴初始位置
DEFAULT_Y -> Y轴初始位置

MAX_ZOOM -> 最大的缩放
MIN_ZOOM -> 最小缩放

ZOOM_OUT_STEP -> 最大的放大次数
ZOOM_IN_STEP  -> 最大的缩小次数 

SHOW_POS -> 是否显示测试坐标（废除）

### 常用指令

ml -> 左移视角
mr -> 又移视角
md -> 下移视角
mu -> 上移视角

zoomxin -> X轴放大
zoomxout -> X轴缩小
zoomyxin -> Y轴放大
zoomyout -> Y轴缩小

draw -> 绘制

delete [name] -> 删除名为name的函数

clear -> 清除所有函数


### 使用事项

函数语法： [name] = [formula]

#### 注意：函数内必须包含 x ，且不支持a,b,c...

一个正确的函数例子:
  y = x ** 2
  
  (使用python的语法)
