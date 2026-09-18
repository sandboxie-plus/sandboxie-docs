# 标题栏中的沙盒名称

_BoxNameTitle_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它控制 Sandboxie 是否在属于沙盒化应用程序的窗口标题栏中显示沙盒名称。

用法：

```
   .
   .
   .
   [DefaultBox]
   BoxNameTitle=y
```

默认情况下，Sandboxie 只在属于沙盒化应用程序的窗口标题栏中显示沙盒化 [#] 指示符。例如：

[#] Sandboxie - Front Page - Windows Internet Explorer [#]

指定 _BoxNameTitle=y_ 会把沙盒名称放入标题栏：

[#] [DefaultBox] Sandboxie - Front Page - Windows Internet Explorer [#]

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 外观](AppearanceSettings.md)
