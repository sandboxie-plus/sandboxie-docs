# 不要复制

_DontCopy_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 0.6.5 起可用。它指定宿主机文件的路径模式，匹配文件的内容不会迁移到沙盒中。

用法：

`DontCopy=[program,]pattern`

```ini
[DefaultBox]
DontCopy=*.iso
DontCopy=media-player.exe,*\Media\*.mkv
```

每条 _DontCopy_ 配置对应一条规则，可重复添加。逗号前的可选前缀用于将规则限定到指定程序，参见[程序名称前缀](ProgramNamePrefix.md)。路径模式的格式与 [OpenFilePath](OpenFilePath.md) 相同。匹配不区分大小写，以宿主机文件的真实路径为准。`*` 匹配任意长度的字符序列，包括路径分隔符；`?` 匹配单个字符。

使用程序名称前缀时，当前设置定义要求将路径中的驱动器或设备部分写成通配符，例如 `*\Media\*.mkv`。在限定程序的规则中，不要使用 `D:\Media\*.mkv` 这样的固定驱动器路径，也不要依赖会展开为完整路径的[可展开变量](ExpandableVariables.md)。

普通的只读访问不需要迁移，会继续使用宿主机文件。当沙盒内的程序请求某项操作，Sandboxie 原本需要将已有文件迁移到沙盒中供其修改时，此规则才会参与判断。初次迁移时若文件匹配规则，Sandboxie 不会创建包含宿主机文件内容的副本：

- 未配置 [CopyBlockDenyWrite](CopyBlockDenyWrite.md) 或设为 `n` 时，Sandboxie 会从请求中移除写入和删除权限，然后重试打开宿主机文件。因此，包含读取权限的请求可能以只读方式成功打开。若请求仅包含写入权限、创建或打开方式不兼容，或受宿主机权限限制，打开操作仍可能失败。
- 若为该程序设置了 _CopyBlockDenyWrite=y_，则此次依赖迁移的打开操作会返回“拒绝访问”。

_DontCopy_ 不会授予 [OpenFilePath](OpenFilePath.md) 那样的直接访问权限，绝不会允许沙盒内的程序写入宿主机文件。已有沙盒副本通常无需初次迁移，但 [CopyNewer](CopyNewer.md) 触发刷新时，刷新中的迁移仍可能检查 _DontCopy_。匹配的规则可以阻止刷新，同时保留已有沙盒副本供程序使用；它不会删除或替换该副本。

未配置 _DontCopy_ 或没有匹配项时，此规则不会阻止迁移；Sandboxie 会采用其他匹配的迁移规则，或按常规大小判断决定如何处理。

_DontCopy_ 在 [CopyLimitKb](CopyLimitKb.md) 之前判断，因此文件大小和 [CopyLimitSilent](CopyLimitSilent.md) 不会改变此规则的处理结果。它也优先于匹配的 [CopyAlways](CopyAlways.md) 和 [CopyEmpty](CopyEmpty.md) 规则。[CopyNewer](CopyNewer.md) 针对已有的沙盒副本，不参与初次迁移方式的选择。

请注意，只有已有的普通宿主机文件原本需要迁移内容时，才会检查此规则。它不控制目录、新建文件，以及无需复制宿主机文件内容的创建、覆盖或删除操作。

启用 [NotifyNoCopy](NotifyNoCopy.md) 后，迁移尝试若匹配此规则，移除写入和删除权限后重试的模式会产生 SBIE2115，拒绝写入模式会产生 SBIE2114。刷新期间，这些消息描述的是迁移决定，不一定代表已有沙盒副本最终能否打开。

可以在 SandMan 的沙盒选项 > 常规选项 > 文件迁移中管理复制规则。此规则类型对应**不要复制**。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[CopyAlways](CopyAlways.md)、[CopyEmpty](CopyEmpty.md)、[CopyNewer](CopyNewer.md)、[CopyBlockDenyWrite](CopyBlockDenyWrite.md)、[NotifyNoCopy](NotifyNoCopy.md)。另请参阅[文件迁移设置](FileMigrationSettings.md)。
