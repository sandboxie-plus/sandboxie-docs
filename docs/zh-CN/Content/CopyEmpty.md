# 复制空的副本

_CopyEmpty_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 0.6.5 起可用。它指定宿主机文件的路径模式：迁移匹配文件时，Sandboxie 会在沙盒中创建长度为零的副本，不复制宿主机文件的内容。

用法：

`CopyEmpty=[program,]pattern`

```ini
[DefaultBox]
CopyEmpty=*\Cache\*.log
CopyEmpty=indexer.exe,*\SearchData\*.db
```

每条 _CopyEmpty_ 配置对应一条规则，可重复添加。逗号前的可选前缀用于将规则限定到指定程序，参见[程序名称前缀](ProgramNamePrefix.md)。路径模式的格式与 [OpenFilePath](OpenFilePath.md) 相同。匹配不区分大小写，以宿主机文件的真实路径为准。`*` 匹配任意长度的字符序列，包括路径分隔符；`?` 匹配单个字符。

使用程序名称前缀时，当前设置定义要求将路径中的驱动器或设备部分写成通配符，例如 `*\Cache\*.log`。在限定程序的规则中，不要使用 `C:\Cache\*.log` 这样的固定驱动器路径，也不要依赖会展开为完整路径的[可展开变量](ExpandableVariables.md)。

已有的普通文件需要迁移且匹配此规则时，Sandboxie 会打开宿主机文件以获取文件信息，创建对应的沙盒文件，并将内容长度设为零。宿主机文件保持不变。随后，沙盒内的程序可以使用这个空副本，并向其中写入新内容。

此规则在 [CopyLimitKb](CopyLimitKb.md) 之前选定，因此创建空副本不受宿主机文件大小的限制。[CopyLimitSilent](CopyLimitSilent.md) 不影响此规则。若启用了 [NotifyNoCopy](NotifyNoCopy.md)，此次迁移尝试会产生 SBIE2113 消息，报告未复制文件内容。

未配置 _CopyEmpty_ 或没有匹配项时，Sandboxie 会采用其他匹配的迁移规则，或按常规大小判断决定如何处理。规则重叠时，[DontCopy](DontCopy.md) 优先于 [CopyAlways](CopyAlways.md)，_CopyAlways_ 优先于 _CopyEmpty_。[CopyNewer](CopyNewer.md) 针对已有沙盒副本单独判断，不改变初次迁移时选择空副本的方式。

请注意以下限制：

- 已有的普通宿主机文件原本需要迁移内容时，会检查 _CopyEmpty_，包括 [CopyNewer](CopyNewer.md) 刷新期间尝试的迁移。
- 此规则本身不会触发已有沙盒副本的刷新。_CopyNewer_ 触发刷新后，匹配的 _CopyEmpty_ 规则可以选择用空副本替换已有副本。
- 此规则不影响目录、仅在沙盒内创建的文件，以及 Sandboxie 无需复制宿主机文件内容的覆盖、删除或创建操作。
- Sandboxie 仍需能够打开宿主机上的对象并查询其文件信息。如果这一步失败，迁移可能失败，而不会生成空副本。

可以在 SandMan 的沙盒选项 > 常规选项 > 文件迁移中管理复制规则。此规则类型对应**复制空的副本**。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[CopyAlways](CopyAlways.md)、[DontCopy](DontCopy.md)、[CopyNewer](CopyNewer.md)、[NotifyNoCopy](NotifyNoCopy.md)、[CopyLimitKb](CopyLimitKb.md)。另请参阅[文件迁移设置](FileMigrationSettings.md)。
