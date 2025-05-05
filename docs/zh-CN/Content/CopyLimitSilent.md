# 复制限制静默模式

_CopyLimitSilent_ 是 [沙盘配置文件](SandboxieIni.md) 中的一项沙箱设置。通常将其指定为 _CopyLimitSilent=y_（请参阅 [是或否设置](YesOrNoSettings.md)），这表示沙盘不应发出警报消息 [SBIE2102](SBIE2102.md)。

用法：

```
   .
   .
   .
   [DefaultBox]
   CopyLimitSilent=y
```

相关的 [沙盘配置文件](SandboxieIni.md) 设置：[CopyLimitKb](CopyLimitKb.md)。
