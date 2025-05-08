# 复制限制 KB

_CopyLimitKb_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。被沙盒程序修改的现有文件必须先复制到沙盒中。此设置指定此复制操作的文件大小限制。大于限制的文件将不会被复制到沙盒中，并且不能被沙盒程序修改。限制以千字节为单位指定（1 千字节 = 1024 字节）。

更多信息，请参见 [SBIE2102](SBIE2102.md)。

用法：

```
   .
   .
   .
   [DefaultBox]
   CopyLimitKb=128000
```

此示例指定只有小于（约）128MB 的文件才会在需要时被复制到 _DefaultBox_ 沙盒中。大于此限制的文件只能被沙盒程序读取，不能更新。

默认设置为 49152 千字节，即 48 兆字节。为一个沙盒设置 _CopyLimitKb_ 的值不会更改其他沙盒的默认值。

大小限制和警报消息可以在 [沙盒设置 > 文件迁移](FileMigrationSettings.md) 中配置。

相关的 [Sandboxie Ini](SandboxieIni.md) 设置：[静默复制限制](CopyLimitSilent.md) 