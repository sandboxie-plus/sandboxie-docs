# 复制限制 Kb

_CopyLimitKb_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。沙盒化程序修改的现有文件必须首先被复制到沙盒中。此设置指定此复制操作的文件大小限制。大于限制的文件不会被复制到沙盒中，沙盒化程序也无法修改它们。限制以千字节为单位指定（1 千字节 = 1024 字节）。

更多信息参见 [SBIE2102](SBIE2102.md)。

用法：

```
   .
   .
   .
   [DefaultBox]
   CopyLimitKb=128000
```

此示例指定：需要时，只有小于（约）128MB 的文件才会被复制到沙盒 _DefaultBox_ 中。大于此限制的文件只能被沙盒化程序读取，不能被更新。

默认设置为 49152 千字节，即 48 兆字节。为一个沙盒把 _CopyLimitKb_ 设为某个值，不会改变其他沙盒的默认值。

大小限制和警报消息可以在 [沙盒设置 > 文件迁移](FileMigrationSettings.md) 中配置。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[复制限制静默](CopyLimitSilent.md)
