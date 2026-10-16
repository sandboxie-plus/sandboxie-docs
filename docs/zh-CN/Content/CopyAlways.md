# 始终复制

_CopyAlways_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 0.6.5 起可用。它指定宿主机文件的路径模式：当沙盒内的程序需要沙盒副本时，匹配的文件应连同内容一起迁移。

用法：

`CopyAlways=[program,]pattern`

```ini
[DefaultBox]
CopyAlways=C:\Data\Reference\*.db
CopyAlways=reporter.exe,*\Reports\*.csv
```

每条 _CopyAlways_ 配置对应一条规则，可重复添加。逗号前的可选前缀用于将规则限定到指定程序，参见[程序名称前缀](ProgramNamePrefix.md)。路径模式的格式与 [OpenFilePath](OpenFilePath.md) 相同。匹配不区分大小写，以宿主机文件的真实路径为准。`*` 匹配任意长度的字符序列，包括路径分隔符；`?` 匹配单个字符。

使用程序名称前缀时，当前设置定义要求将路径中的驱动器或设备部分写成通配符，例如 `*\Reports\*.csv`。在限定程序的规则中，不要使用 `C:\Reports\*.csv` 这样的固定驱动器路径，也不要依赖会展开为完整路径的[可展开变量](ExpandableVariables.md)。

通常，只有沙盒内的程序请求的操作需要沙盒副本时，Sandboxie 才会迁移已有的宿主机文件。如果文件匹配 _CopyAlways_，Sandboxie 会在检查 [CopyLimitKb](CopyLimitKb.md) 之前选择迁移完整内容。因此，匹配的迁移不受所设大小阈值的限制，也不会触发大文件提示；[CopyLimitSilent](CopyLimitSilent.md) 对它没有影响。

未配置 _CopyAlways_ 或没有匹配项时，Sandboxie 会采用其他匹配的迁移规则，或按常规大小判断决定如何处理。规则重叠时，[DontCopy](DontCopy.md) 优先于 _CopyAlways_，_CopyAlways_ 优先于 [CopyEmpty](CopyEmpty.md)。[CopyNewer](CopyNewer.md) 单独处理已有沙盒副本的刷新。_CopyAlways_ 本身不会触发刷新，但刷新过程中若匹配此规则，会在常规大小限制和提示判断之前选择迁移完整内容。

请注意以下限制：

- 只有已有的普通宿主机文件需要迁移内容时，才会检查此规则。它本身不会触发已有沙盒副本的刷新，也不控制新建文件、目录，以及无需复制宿主机文件内容的创建或覆盖操作。
- 此规则可覆盖迁移大小判断，但无法保证读取不可访问的宿主机文件内容，也不会绕过宿主机文件的访问限制。如果 Sandboxie 无法按迁移要求访问源文件，迁移可能失败，也可能继续进行但不复制文件内容。
- 宿主机文件不会被修改，后续写入会作用于沙盒副本。

可以在 SandMan 的沙盒选项 > 常规选项 > 文件迁移中管理复制规则。此规则类型对应**始终复制**。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[DontCopy](DontCopy.md)、[CopyEmpty](CopyEmpty.md)、[CopyNewer](CopyNewer.md)、[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)。另请参阅[文件迁移设置](FileMigrationSettings.md)。
