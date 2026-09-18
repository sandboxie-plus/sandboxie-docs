# 互联网访问被拒绝时通知

_NotifyInternetAccessDenied_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。通常指定为 _NotifyInternetAccessDenied=y_，表示当程序被拒绝访问互联网时，Sandboxie 应发出 [SBIE1307](SBIE1307.md) 消息。

用法：
```
   .
   .
   .
   [DefaultBox]
   NotifyInternetAccessDenied=y
```

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 互联网访问](RestrictionsSettings.md#互联网访问)

相关 [沙盒管理器](SandboxieControl.md) 设置：[程序设置](ProgramSettings.md#页面-2)
