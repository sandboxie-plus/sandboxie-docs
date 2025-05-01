# 标题栏中的沙箱名称

_BoxNameTitle_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于控制 Sandboxie 是否在属于某个沙箱应用程序的窗口标题栏中显示沙箱名称。

用法：

```
   .
   .
   .
   [DefaultBox]
   BoxNameTitle=y
```

默认情况下，Sandboxie 只会在属于沙箱应用程序的窗口标题栏中显示沙箱 [#] 指示符。例如：

[#] Sandboxie - Front Page - Windows Internet Explorer [#]

如果指定 _BoxNameTitle=y_ ，则会在标题栏中显示沙箱名称：

[#] [DefaultBox] Sandboxie - Front Page - Windows Internet Explorer [#]

相关的 [沙箱控制](SandboxieControl.md) 设置： [沙箱设置 > 外观](AppearanceSettings.md)
