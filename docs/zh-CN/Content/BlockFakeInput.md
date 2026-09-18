# 阻止伪造输入

**此功能已在 SBIE 4.0 及更高版本中移除，不再可用。**

_BlockFakeInput_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 Sandboxie 是否应允许沙盒化程序制造伪造的键盘输入，并将其发送到该沙盒外运行的应用程序的窗口。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockFakeInput=n
```

键盘输入由活动的高亮窗口接收。无论键盘输入是由程序制造的（伪造输入），还是来自键盘（真实输入），都是如此。

默认情况下，Sandboxie 会允许沙盒中运行的程序制造伪造输入，前提是接收窗口属于在同一沙盒中运行的应用程序。

如果伪造输入最终会进入该沙盒外的窗口，Sandboxie 将丢弃该输入并发出 [SBIE1304](SBIE1304.md) 消息。

指定 _BlockFakeInput=n_ 表示应允许沙盒化程序制造伪造键盘输入，无论该输入的接收者是谁。

要试验此设置，你可以运行 Windows 屏幕键盘 _osk.exe_ 的沙盒化实例。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 硬件访问](RestrictionsSettings.md#从-sandboxie-v4-及更高版本开始-硬件访问功能已被移除)
