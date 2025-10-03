# 互联网访问被拒绝时通知

_NotifyInternetAccessDenied_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。通常写作 _NotifyInternetAccessDenied=y_，该设置表示当程序被拒绝访问互联网时，沙盘应发出 [SBIE1307](SBIE1307.md) 消息。

用法:
```ini
   .
   .
   .
   [DefaultBox]
   NotifyInternetAccessDenied=y
```

相关的 [沙盘控制](SandboxieControl.md) 设置： [沙箱设置 > 限制 > 互联网访问](RestrictionsSettings.md#internet-access)。

相关的 [沙盘控制](SandboxieControl.md) 设置： [程序设置](ProgramSettings.md#page-2)。