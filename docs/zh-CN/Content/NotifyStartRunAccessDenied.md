# 启动/运行访问被拒绝时通知

_NotifyStartRunAccessDenied_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。它通常被设置为 _NotifyStartRunAccessDenied=y_，用于指示沙盘在程序因被拒绝启动或运行时，发出 [SBIE1308](SBIE1308.md) 消息。

用法示例：
```
   .
   .
   .
   [DefaultBox]
   NotifyStartRunAccessDenied=y
```

相关的 [沙盘控制](SandboxieControl.md) 设置：[沙箱设置 > 限制 > 启动/运行访问](RestrictionsSettings.md#startrun-access)。
相关的 [沙盘控制](SandboxieControl.md) 设置：[程序设置](ProgramSettings.md#page-2)。