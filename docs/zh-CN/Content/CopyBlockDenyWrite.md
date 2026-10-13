# 不复制时拒绝写入

_CopyBlockDenyWrite_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 0.6.5 起可用。当 Sandboxie 决定不复制宿主机文件时，此设置控制依赖文件迁移的打开操作如何处理。

用法：

```ini
[DefaultBox]
CopyBlockDenyWrite=y
CopyBlockDenyWrite=viewer.exe,n
```

语法为 `CopyBlockDenyWrite=[program,]y|n`。可选的[程序名称前缀](ProgramNamePrefix.md)可将该值限定为仅适用于指定的可执行文件。可以通过多条配置为不同程序设置不同的值，但此项是“是或否”设置，不是路径列表。

对于初次迁移，若设为 `y`，当迁移判断选择**不复制**时，需要沙盒副本的文件打开操作将返回“拒绝访问”。未设置此项或设为 `n` 时，Sandboxie 会移除请求中的写入和删除权限，然后重试打开宿主机文件。因此，包含读取权限的请求可能以只读方式成功打开文件；若移除这些权限后仍无法满足请求，打开操作仍可能失败。

**不复制**的决定可能来自匹配的 [DontCopy](DontCopy.md) 规则，也可能来自 [CopyLimitKb](CopyLimitKb.md) 控制的常规大小判断，包括大文件提示无法获得答复或用户拒绝迁移的情况。此设置本身不会选择文件，也不会阻止原本能够成功的迁移。

匹配的 [CopyAlways](CopyAlways.md) 和 [CopyEmpty](CopyEmpty.md) 规则会选择相应的复制模式，_CopyBlockDenyWrite_ 不作用于这些结果。当 [CopyNewer](CopyNewer.md) 发起刷新时，此设置可能影响刷新迁移的结果。刷新失败不一定会阻止随后打开已有的沙盒副本。

[CopyLimitSilent](CopyLimitSilent.md) 仅控制因大小限制而拒绝迁移时的 SBIE2102 消息，不改变迁移决定。对于显式 _DontCopy_ 规则，启用 [NotifyNoCopy](NotifyNoCopy.md) 后，此设置为 `y` 时会产生 SBIE2114，为 `n` 时会产生 SBIE2115。这些消息描述的是选中的模式，不代表刷新尝试后打开已有副本的最终结果。

在 SandMan 中，打开“沙盒选项 > 常规选项 > 文件迁移”。复选框的表述方向与此设置相反：**当一个文件不能被迁移时，尝试以只读模式打开它**。取消勾选该项会启用 `CopyBlockDenyWrite=y`。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[DontCopy](DontCopy.md)、[CopyAlways](CopyAlways.md)、[CopyEmpty](CopyEmpty.md)、[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)、[NotifyNoCopy](NotifyNoCopy.md)。另请参阅[文件迁移设置](FileMigrationSettings.md)。
