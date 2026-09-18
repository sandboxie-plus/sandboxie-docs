# 对快速恢复使用自动恢复忽略

_UseAutoRecoverIgnoreForQuick_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 1.18.0 起可用。它指定 [自动恢复忽略](AutoRecoverIgnore.md) 排除列表是否也应用于 [快速恢复](QuickRecovery.md) 窗口，从可恢复文件列表中隐藏匹配的文件。

用法：

```
   .
   .
   .
   [DefaultBox]
   UseAutoRecoverIgnoreForQuick=n
```

此设置默认启用。把它设为 _n_ 可在快速恢复窗口中显示所有可恢复文件，包括匹配 [自动恢复忽略](AutoRecoverIgnore.md) 模式的文件。

注意：这仅在快速恢复窗口中的"显示全部"复选框未被勾选时才生效。

在沙盒管理器中，这对应"使用上述排除列表在快速恢复窗口中隐藏匹配文件"复选框，位于沙盒选项 > 文件恢复 > 即时恢复下。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[自动恢复忽略](AutoRecoverIgnore.md)、[恢复文件夹](RecoverFolder.md)。另请参阅 [快速恢复](QuickRecovery.md)。
