# 覆盖沙箱窗口

_CoverBoxedWindows_ 是 [Sandboxie Ini](SandboxieIni.md) 中自 v1.13.6 / 5.68.6 版本起提供的沙箱配置选项。启用后，它会阻止主机进程对沙箱内的进程进行屏幕截图。

```
   .
   .
   .
   [DefaultBox]
   CoverBoxedWindows=y
```

与 _CoverBoxedWindows_ 类似的设置还有 [阻止屏幕捕获](BlockScreenCapture.md)。

相关的 Sandboxie Plus 选项：沙箱选项 > 安全选项 > 沙箱保护 > 防止进程从被沙箱化的窗口捕获窗口图像