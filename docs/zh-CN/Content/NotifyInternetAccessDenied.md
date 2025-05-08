# 通知互联网访问被拒绝

_NotifyInternetAccessDenied_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它通常指定为 _NotifyInternetAccessDenied=y_，表示当程序被拒绝访问互联网时，Sandboxie 应发出消息 [SBIE1307](SBIE1307.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   NotifyInternetAccessDenied=y
```

相关的 [Sandboxie 控制](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 互联网访问](RestrictionsSettings.md#internet-access)

相关的 [Sandboxie 控制](SandboxieControl.md) 设置：[程序设置](ProgramSettings.md#page-2) 