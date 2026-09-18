# 恢复文件夹

_RecoverFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 [快速恢复](QuickRecovery.md) 应检查的沙盒化文件夹。可以指定 [个人文件夹](ShellFolders.md)。例如：
```
   .
   .
   .
   [DefaultBox]
   RecoverFolder=%Personal%
   RecoverFolder=C:\Downloads
   [InstallBox]
   RecoverFolder=D:\Program Files
```

前两个示例设置指定：从 DefaultBox 沙盒执行 [快速恢复](QuickRecovery.md) 时，应在 C 盘的_文档_和_下载_文件夹中查找。

第三个示例设置指定：从 InstallBox 沙盒执行快速恢复时，应在 D 盘的 _Program Files_ 文件夹中查找。

注意：[快速恢复](QuickRecovery.md) 在指定文件夹中查找时，也会在该文件夹内的任何文件夹、以及那些文件夹内的任何文件夹中查找，深度不限。

自 Sandboxie Plus 1.18.0 起，文件夹路径可以包含通配符 `*`（匹配任意数量字符）、`?`（匹配单个字符）和 `**`（匹配任意数量字符，包括路径分隔符）。路径会以其 NT、DOS 和网络别名形式进行匹配。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 恢复 > 快速恢复](RecoverySettings.md#快速恢复)
