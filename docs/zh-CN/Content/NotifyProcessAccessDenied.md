# 进程访问被拒绝时通知

_NotifyProcessAccessDenied_ 是一个自 v1.0.16 / 5.55.16 起添加到 [Sandboxie Ini](SandboxieIni.md) 的沙箱设置。它通常以 _NotifyProcessAccessDenied=y_ 的形式指定，表示当程序被拒绝读取进程的地址空间时，沙盘会发出 [SBIE2111](SBIE2111.md) 消息。

用法：
```ini
   .
   .
   .
   [DefaultBox]
   NotifyProcessAccessDenied=y
```

相关的 Sandboxie Plus 设置路径为：沙箱选项 > 常规选项 > 限制 > 其他限制 > 当进程访问被拒绝时发出 2111 消息。

更多信息，请参见 [SBIE2111](SBIE2111.md)。