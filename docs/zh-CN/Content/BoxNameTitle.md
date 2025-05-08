# 沙盒名称标题

_BoxNameTitle_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它控制 Sandboxie 是否在属于沙盒化应用程序的窗口的标题栏中显示沙盒的名称。

用法：

```
   .
   .
   .
   [DefaultBox]
   BoxNameTitle=y
```

默认情况下，Sandboxie 只在属于沙盒化应用程序的窗口的标题栏中显示沙盒化 [#] 指示器。例如：

[#] Sandboxie - 首页 - Windows Internet Explorer [#]

指定 _BoxNameTitle=y_ 会在标题栏中放置沙盒名称：

[#] [DefaultBox] Sandboxie - 首页 - Windows Internet Explorer [#]

相关 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 外观](AppearanceSettings.md) 