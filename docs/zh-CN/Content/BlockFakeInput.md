# 阻止虚假输入

**此功能已在 SBIE 版本 4 及更高版本中移除。它不再可用。**

_BlockFakeInput_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否应该允许沙盒化程序生成虚假键盘输入并将其发送到该沙盒外运行的应用程序的窗口。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockFakeInput=n
```

键盘输入由活动的、高亮显示的窗口接收。无论键盘输入是由程序生成的（虚假输入），还是来自键盘的（真实输入），这一点都是成立的。

默认情况下，Sandboxie 允许在沙盒中运行的程序生成虚假输入，前提是接收窗口属于在同一沙盒中运行的应用程序。

如果虚假输入将最终进入该沙盒外的窗口，Sandboxie 将丢弃该输入并发出消息 [SBIE1304](SBIE1304.md)。

指定 _BlockFakeInput=n_ 表示应该允许沙盒化程序生成虚假键盘输入，无论该输入的接收者是谁。

要试验此设置，您可以运行沙盒化的 _osk.exe_，即 Windows 屏幕键盘。

相关 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 硬件访问](RestrictionsSettings.md#hardware-access-has-been-removed-from-sandboxie-v4-and-up) 