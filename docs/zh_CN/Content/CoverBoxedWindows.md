# 覆盖沙盒窗口

_CoverBoxedWindows_ 是 [Sandboxie Ini](SandboxieIni.md) 中自 v1.13.6 / 5.68.6 版本起提供的沙盒配置选项。启用后，它会阻止主机进程对沙盒内的进程进行屏幕截图。

```
   .
   .
   .
   [DefaultBox]
   CoverBoxedWindows=y
```

与 _CoverBoxedWindows_ 类似的设置还有 [阻止屏幕捕获](BlockScreenCapture.md)。

相关的 Sandboxie Plus 选项：沙盒选项 > 安全选项 > 沙盒保护 > 防止进程从被沙盒化的窗口捕获窗口图像