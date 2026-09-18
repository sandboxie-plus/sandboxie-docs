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

通常，一旦文件被复制到沙盒中（参见 [文件迁移设置](FileMigrationSettings.md)），沙盒化程序会继续使用该副本，即使宿主上的原始文件后来被更改。当文件路径匹配 _CopyNewer_ 模式时，Sandboxie 会在每次打开文件时比较宿主文件的最后写入时间与沙盒副本；如果宿主文件较新，在打开完成前会把新副本迁移到沙盒中。

请注意以下限制：

- 只适用于已在沙盒内有副本的常规文件正常打开时。
- 不适用于文件的初始迁移、目录、只写打开、已删除文件或创建/覆盖操作。
- 模式匹配不区分大小写，应用于宿主（真实）文件路径。
- 如果刷新已在进行中或失败，现有沙盒副本仍可供程序使用。

复制规则（包括"复制较新文件"类型规则）可以在沙盒管理器的沙盒选项 > 常规选项 > 文件迁移下管理。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[复制限制 Kb](CopyLimitKb.md)、[复制限制静默](CopyLimitSilent.md)。另请参阅 [文件迁移设置](FileMigrationSettings.md)。
