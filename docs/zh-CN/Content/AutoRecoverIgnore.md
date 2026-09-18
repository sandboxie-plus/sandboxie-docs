# 自动恢复忽略

_AutoRecoverIgnore_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 [快速恢复](QuickRecovery.md) 的即时恢复扩展应忽略的文件夹或文件类型。例如：

```
   .
   .
   .
   [DefaultBox]
   AutoRecoverIgnore=.part
   AutoRecoverIgnore=%Desktop%
   AutoRecoverIgnore=C:\Folder
```

第一个示例把任何以 _.part_ 结尾的文件排除在即时恢复之外。这些文件由 Mozilla 浏览器的下载管理器创建，代表未完成的下载。下载完成时，_.part_ 扩展名会从文件移除，使其符合即时恢复条件。注意：_.part_ 是默认设置。

第二个和第三个示例把指定文件夹排除在即时恢复之外。

自 Sandboxie Plus 1.18.0 起，条目可以包含通配符 `*`（匹配任意数量字符）、`?`（匹配单个字符）和 `**`（匹配任意数量字符，包括路径分隔符）。路径会以其 NT、DOS 和网络别名形式进行匹配。

自 Sandboxie Plus 1.18.0 起，排除列表也可以应用于 [快速恢复](QuickRecovery.md) 窗口；参见 [对快速恢复使用自动恢复忽略](UseAutoRecoverIgnoreForQuick.md)。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 恢复 > 即时恢复](RecoverySettings.md#即时恢复)
