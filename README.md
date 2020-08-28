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

这里引入 Tap-key 功能，Tap-key通过短按和长按两种功能，短按用作正常按键，长按不放则激活额外的功能。

### <kbd>D</kbd> 键导航

这里将 <kbd>D</kbd> 被用作Tap-key。短按，输出`d`；长按<kbd>D</kbd>不放，则激活移动光标功能，<kbd>H</kbd>、<kbd>J</kbd>、<kbd>K</kbd>、<kbd>L</kbd>被映射为方向键，而 <kbd>U</kbd> 和 <kbd>N</kbd> 则为 <kbb>PgUp</kbd> 和 <kbd>PgDn</kbd>。

![](img/d-for-navigation.png)

+ <kbd>d</kbd> + <kbd>h</kbd> → <kbd>←</kbd>
+ <kbd>d</kbd> + <kbd>j</kbd> → <kbd>↓</kbd>
+ <kbd>d</kbd> + <kbd>k</kbd> → <kbd>↑</kbd>
+ <kbd>d</kbd> + <kbd>l</kbd> → <kbd>→</kbd>
+ <kbd>d</kbd> + <kbd>u</kbd> → <kbd>PgUp</kbd>
+ <kbd>d</kbd> + <kbd>n</kbd> → <kbd>PgDn</kbd>

### <kbd>;</kbd> 键用作 <kbd>Ctrl</kbd>

<kbd>;</kbd>也被用作Tap-key，短按输出`;`，长按用作<kbd>Ctrl</kbd>。

![](https://github.com/xiongyihui/keyboard/raw/master/img/semicolon_as_ctrl.png)

+ <kbd>;</kbd> + <kbd>c</kbd> = <kbd>Ctrl</kbd> + <kbd>c</kbd>
+ <kbd>;</kbd> + <kbd>v</kbd> = <kbd>Ctrl</kbd> + <kbd>v</kbd>
+ <kbd>;</kbd> + <kbd>x</kbd> = <kbd>Ctrl</kbd> + <kbd>x</kbd>
+ <kbd>;</kbd> + <kbd>a</kbd> = <kbd>Ctrl</kbd> + <kbd>a</kbd>

在VS Code里面双手打字时，用左右手配合按<kbd>;</kbd> + <kbd>C</kbd>比左手按<kbd>Ctrl</kbd> + <kbd>C</kbd>要方便一些。值得一提的是，VS Code中未选中文本时，<kbd>Ctrl</kbd> + <kbd>C</kbd>是复制光标所在的行，之后<kbd>Ctrl</kbd> + <kbd>V</kbd>，则把复制的行粘贴到光标下新的一行。再配合<kbd>D</kbd> + <kbd>H</kbd>、<kbd>J</kbd>、<kbd>K</kbd>、<kbd>L</kbd>移动光标，可以很便捷。

而在浏览器中，可用<kbd>;</kbd> + <kbd>Tab</kbd>替代<kbd>Ctrl</kbd> + <kbd>Tab</kbd>切换标签页，<kbd>;</kbd> + <kbd>T</kbd>打开新标签页，<kbd>;</kbd> + <kbd>W</kbd>关闭标签页。

### 结对快捷键 (Pair-Keys)
另外，键盘还支持同时（或10ms以内）按下两个键触发特殊功能，这里称之为结对快捷键（pair-keys）。

## Todo
- [ ] 添加鼠标功能
- [ ] 添加炫酷的灯效


## 致谢
+ [MicroPython](https://github.com/micropython/micropython)
+ [CircuitPython](https://github.com/adafruit/circuitpython)
+ [TMK](https://github.com/tmk/tmk_keyboard)
+ [Toward a more useful keyboard](https://github.com/jasonrudolph/keyboard)


[1]: https://github.com/makerdiary/python-keyboard
