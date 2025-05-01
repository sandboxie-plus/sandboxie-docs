# 复制限制 Kb

_CopyLimitKb_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置项。要在沙箱中修改现有文件，必须首先将文件复制到沙箱中。本设置用于指定此复制操作的文件大小上限。大于此限制的文件将不会被复制进沙箱，沙箱程序也无法对其进行修改。该限制的单位为千字节（1 千字节 = 1024 字节）。

欲了解更多信息，请参阅 [SBIE2102](SBIE2102.md)。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   CopyLimitKb=128000
```

此示例表示，仅当所需文件小于（约）128 MB 时，才会被复制进 _DefaultBox_ 沙箱。超过此限制的文件，沙箱程序只能读取，无法更新。

默认设置为 49152 千字节，即 48 兆字节。为某个沙箱单独设置 _CopyLimitKb_ 并不会影响其他沙箱的默认值。

可在 [沙箱设置 > 文件迁移](FileMigrationSettings.md) 中配置大小限制及警告消息。

相关的 [Sandboxie Ini](SandboxieIni.md) 设置项：[复制限制静默](CopyLimitSilent.md)