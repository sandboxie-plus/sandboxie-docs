# 通知启动运行访问被拒绝

_NotifyStartRunAccessDenied_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它通常指定为 _NotifyStartRunAccessDenied=y_，表示当程序被拒绝启动或运行时，Sandboxie 应发出消息 [SBIE1308](SBIE1308.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   NotifyStartRunAccessDenied=y
```

相关 [Sandboxie 控制](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 启动/运行访问](RestrictionsSettings.md#startrun-access) 相关 [Sandboxie 控制](SandboxieControl.md) 设置：[程序设置](ProgramSettings.md#page-2) 