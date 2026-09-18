# 启动/运行访问被拒绝时通知

_NotifyStartRunAccessDenied_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。通常指定为 _NotifyStartRunAccessDenied=y_，表示当程序被拒绝启动或运行时，Sandboxie 应发出 [SBIE1308](SBIE1308.md) 消息。

用法：
```
   .
   .
   .
   [DefaultBox]
   NotifyStartRunAccessDenied=y
```

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 启动/运行访问](RestrictionsSettings.md#启动-运行访问)
相关 [沙盒管理器](SandboxieControl.md) 设置：[程序设置](ProgramSettings.md#页面-2)
