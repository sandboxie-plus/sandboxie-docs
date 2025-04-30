# 阻止屏幕截图

_BlockScreenCapture_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置，自 v1.13.6 / 5.68.6 版本起可用。启用该选项后，将阻止沙箱内的进程访问沙箱外窗口的图像。例如：

```
   .
   .
   .
   [DefaultBox]
   BlockScreenCapture=y
```

与 _BlockScreenCapture_ 类似的设置还有 [覆盖沙箱窗口](CoverBoxedWindows.md)。

相关的 Sandboxie Plus 设置：沙箱选项 > 常规选项 > 限制 > 阻止沙箱内进程捕获窗口图像
