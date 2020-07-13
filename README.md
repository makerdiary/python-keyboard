Python Keyboard
===============

  中文 | [English][1]
------|--------------

从手焊一个跑Python的USB蓝牙双模键盘，到设计一个跑Python键盘


![](img/python-inside-keyboard.png)


## 自己手焊键盘

如果想深入了解键盘，最好的方式是自己造一把，可以按照仓库中的 [hand-wiring-a-keyboard.md](hand-wiring-a-keyboard.md)，软硬兼施，手焊一个跑Python键盘。

![](img/colorful-keycaps.jpg)

## 从原型到产品

跑Python的手焊键盘得到了不少反馈，很多人喜欢它，有的人质疑为什么要用Python。 开始只是觉得这很有趣而已，当投入更多时间完善和探索之后，越来越觉得Python可以给键盘带来很独特的非凡体验。 而手焊一个键盘对于很多人来说很难，于是决定设计一个跑Python的新键盘，让更多人能体验Python和键盘结合在一起的惊喜。

跑Python的键盘，不仅是个键盘，也是一个U盘，键盘的Python代码则保存在U盘中，可以用任意文本编辑器修改Python代码，无需配置任何开发环境。 配置键盘的keymap，添加一个新的宏，或者实现一个新功能，变得非常简单——修改U盘中的Python文件，保存后，即刻运行生效。

更多详情见[M60键盘](https://python-keyboard.gitee.io/)。

[![](https://gitee.com/makerdiary/python-keyboard/raw/master/img/m60.jpg)](https://python-keyboard.gitee.io/)

## 更进一步——让键盘更具生产力
这是一个 60% 键盘，缺少了包括 F1~F12、 方向键、小键盘等键位。

但通过引入[ TMK ](https://github.com/tmk/tmk_keyboard/blob/master/tmk_core/doc/keymap.md)中的层级切换和组合按键功能，并融入 [Toward a more useful keyboard](https://github.com/jasonrudolph/keyboard) 中把手指尽量停留在 <kbd>A</kbd>、<kbd>S</kbd>、<kbd>D</kbd>、<kbd>F</kbd> 和 <kbd>J</kbd>、<kbd>K</kbd>、<kbd>L</kbd>、<kbd>;</kbd> 等起始键位的理念，我们可以让这个小键盘更具生产力。

这里引入 Tap-key 功能，即按某个按键不放激活另外的功能。

比如把 <kbd>d</kbd> 用作 Tap-key，即短按 <kbd>d</kbd> 输出 <kbd>d</kbd>， 按住 <kbd>d</kbd> 不放则激活移动光标功能，<kbd>H</kbd>、<kbd>J</kbd>、<kbd>K</kbd>、<kbd>L</kbd>被映射为方向键，而 <kbd>U</kbd> 和 <kbd>N</kbd> 则为 <kbb>PgUp</kbd> 和 <kbd>PgDn</kbd>。

![](img/d-for-navigation.png)

+ <kbd>d</kbd> + <kbd>h</kbd> → <kbd>←</kbd>
+ <kbd>d</kbd> + <kbd>j</kbd> → <kbd>↓</kbd>
+ <kbd>d</kbd> + <kbd>k</kbd> → <kbd>↑</kbd>
+ <kbd>d</kbd> + <kbd>l</kbd> → <kbd>→</kbd>
+ <kbd>d</kbd> + <kbd>u</kbd> → <kbd>PgUp</kbd>
+ <kbd>d</kbd> + <kbd>n</kbd> → <kbd>PgDn</kbd>

要实现这个功能，把 `keyboard.py` 和 `action_code.py` 拷贝键盘的 U 盘中，然后将键盘的 `code.py` 修改为：

```python
# code.py

from keyboard import main

main()
```

另外，这个 Python 键盘还支持了同时按下两个按键 (间隔不超过25ms) 激活特殊功能，也计划支持长按 <kbd>;</kbd> 用作 <kbd>Ctrl</kbd>，用 <kbd>;</kbd> + <kbd>c</kbd> 替代 <kbd>Ctrl</kbd> + <kbd>c</kbd>，在 VS Code 中使用很方便。

## Todo
+ 长按 <kbd>;</kbd> 用作 <kbd>Ctrl</kbd>
+ 宏功能
+ 优化速度


[1]: https://github.com/makerdiary/python-keyboard
