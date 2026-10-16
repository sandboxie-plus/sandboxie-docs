# 复制较新文件

_CopyNewer_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 1.18.1 起可用。它指定一系列文件路径模式，当宿主机上匹配的文件修改时间更新时，刷新文件的现有沙盒副本。

用法：

```
   .
   .
   .
   [DefaultBox]
   CopyNewer=C:\Data\*.txt
```

通常，一旦文件被复制到沙盒中（参见 [文件迁移设置](FileMigrationSettings.md)），沙盒化程序会继续使用该副本，即使宿主上的原始文件后来被更改。当文件路径匹配 _CopyNewer_ 模式时，Sandboxie 会在符合条件的打开操作中比较宿主文件与沙盒副本的最后写入时间；如果宿主文件较新，会在完成打开操作前尝试刷新副本。

刷新时的迁移使用与初次内容迁移相同的规则、大小限制、提示行为和通知机制。匹配的 [DontCopy](DontCopy.md) 规则可阻止刷新；[CopyAlways](CopyAlways.md) 可在进行大小判断和提示前选择完整内容迁移；[CopyEmpty](CopyEmpty.md) 可选择用空副本替换。上述规则本身不会触发刷新。[CopyBlockDenyWrite](CopyBlockDenyWrite.md) 可影响本次刷新迁移的结果，但刷新失败不一定会导致随后打开已有沙盒副本的操作被拒绝。

请注意以下限制：

- 只适用于已在沙盒内有副本的常规文件正常打开时。
- 不适用于文件的初始迁移、目录、已删除文件或创建/覆盖操作。对于 [WriteFilePath](WriteFilePath.md) 等只写资源路径模式，也会跳过刷新；这里并非仅根据应用程序请求的访问权限来判断。
- 模式匹配不区分大小写，应用于宿主（真实）文件路径。
- 如果刷新已在进行中或失败，现有沙盒副本仍可供程序使用。
- 刷新成功并不一定表示已复制完整内容：迁移规则或源文件访问的回退处理都可能使副本内容为空。

复制规则（包括“复制较新的版本”类型规则）可以在 SandMan 的沙盒选项 > 常规选项 > 文件迁移下管理。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[复制限制 Kb](CopyLimitKb.md)、[复制限制静默](CopyLimitSilent.md)。另请参阅 [文件迁移设置](FileMigrationSettings.md)。
