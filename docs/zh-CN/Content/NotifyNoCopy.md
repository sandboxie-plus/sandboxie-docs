# 不复制通知

_NotifyNoCopy_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 1.7.0 起可用。它用于在迁移规则选择不复制宿主机文件的部分或全部内容时发出消息。

用法：

`NotifyNoCopy=y|n`

```ini
[DefaultBox]
NotifyNoCopy=y
```

此项是[是或否设置](YesOrNoSettings.md)，不是路径列表。它适用于配置了此项的沙盒，或从 `[GlobalSettings]` 继承此项的沙盒，不接受程序名称前缀。未设置此项或设为 `n` 时，这些通知默认禁用。

启用后，Sandboxie 会在显式文件迁移规则匹配时发出消息：

- [CopyEmpty](CopyEmpty.md) 选择创建不含宿主机文件内容的副本时，发出 SBIE2113。
- [DontCopy](DontCopy.md) 选择不复制，且启用了 [CopyBlockDenyWrite](CopyBlockDenyWrite.md) 时，发出 SBIE2114；这对应初次迁移时的拒绝写入模式。
- _DontCopy_ 选择不复制，且未启用拒绝写入时，发出 SBIE2115；这对应初次迁移时移除写入和删除权限后重试打开的模式。

消息包含文件名、沙盒名称和宿主机文件大小。它在迁移代码选中匹配的 _CopyEmpty_ 或 _DontCopy_ 规则时产生，不会仅因沙盒内程序读取文件而产生。

[CopyNewer](CopyNewer.md) 没有专用的 _NotifyNoCopy_ 消息。不过，它发起的刷新迁移也可能选中 _CopyEmpty_ 或 _DontCopy_，从而发出相应通知。这些消息描述的是选中的迁移模式，不能证明复制已完成，也不代表最终的文件打开结果。刷新时，即使选择不复制，已有的沙盒副本仍可能可供程序使用，不一定会拒绝打开或重试访问宿主机文件。

_NotifyNoCopy_ 不报告成功的 [CopyAlways](CopyAlways.md) 迁移、未触发此类刷新的已有沙盒副本访问，也不报告一般的底层复制失败。它同样不报告仅因 [CopyLimitKb](CopyLimitKb.md) 大小判断而被拒绝迁移的文件。大小限制消息 SBIE2102 由 [CopyLimitSilent](CopyLimitSilent.md) 单独控制。

在 SandMan 中，打开“沙盒选项 > 常规选项 > 文件迁移”，勾选**当一个文件没有被完全迁移时，提示问题代码: SBIE2113 / SBIE2114 / SBIE2115**。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[CopyEmpty](CopyEmpty.md)、[DontCopy](DontCopy.md)、[CopyBlockDenyWrite](CopyBlockDenyWrite.md)、[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)。另请参阅[文件迁移设置](FileMigrationSettings.md)。
