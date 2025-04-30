# 阻止伪造输入

**该功能自 SBIE 4 版本及以上已被移除，不再可用**

_BlockFakeInput_ 曾是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。它用于指定 Sandboxie 是否允许沙箱中的程序生成伪造的键盘输入，并将其发送到运行在该沙箱外部的应用程序窗口。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   BlockFakeInput=n
```

键盘输入会被当前活动且高亮的窗口接收。无论该键盘输入是否由程序生成（伪造输入），还是来源于物理键盘（真实输入），都是如此。

默认情况下，Sandboxie 允许在沙箱中运行的程序生成伪造输入，只要接收该输入的窗口属于同一沙箱中的应用程序。

如果伪造输入将被发送到该沙箱之外的窗口，Sandboxie 会丢弃该输入，并发出 [SBIE1304](SBIE1304.md) 消息。

指定 _BlockFakeInput=n_ 表示无论输入接收方是谁，沙箱中的程序都被允许生成伪造的键盘输入。

要测试此设置，可以在沙箱中运行 _osk.exe_，即 Windows 屏幕键盘。

相关的 [沙箱控制](SandboxieControl.md) 设置： [沙箱设置 > 限制 > 硬件访问](RestrictionsSettings.md#hardware-access-has-been-removed-from-sandboxie-v4-and-up)
