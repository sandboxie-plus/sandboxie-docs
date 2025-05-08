# 阻止屏幕捕获

_BlockScreenCapture_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置，自 v1.13.6 / 5.68.6 版本起可用。如果启用，它将阻止沙盒化进程访问沙盒外窗口的图像。例如：

```
   .
   .
   .
   [DefaultBox]
   BlockScreenCapture=y
```

与 _BlockScreenCapture_ 类似的设置是 [CoverBoxedWindows](CoverBoxedWindows.md)。

相关 Sandboxie Plus 设置：沙盒选项 > 常规选项 > 限制 > 阻止沙盒化进程捕获窗口图像 