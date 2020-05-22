# 五子棋AI

## 任务

使用`python`实现简单的五子棋AI。

## 要求

将两人的AI放到ais文件夹中，使用`runChess.py`进行对弈，输出胜负结果。

>   在ais文件夹中给出了`demo.py`，本人在阅读源码时写了部分注释。
>
>   查看源码不难发现`demo.py`只是提供核心函数，`runChess.py`也只是调用核心函数输出结果，调试起来颇为不便。因此我实现了一个外接图形界面`selfTest.py`对`demo.py`进行调用，方便个人调试时测试ai的棋力。

## 结构

正确的目录结构：

```bash
.
└── compete
    ├── ais
    │   ├── demo1.py    # a同学ai
    │   └── demo2.py    # b同学ai
    ├── runChess.py     # 对弈
    └── selfTest.py     # 测试单ai棋力
```

## 截图

使用`selfTest.py`测试`demo.py`：

![截图录屏_tk_20200522122522](https://i.loli.net/2020/05/22/LMXQCVGSZrxdO38.png)