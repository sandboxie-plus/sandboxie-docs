# 恢复文件夹

_RecoverFolder_ 是 [沙盘配置文件](SandboxieIni.md) 中的一个沙箱设置。它指定了 [快速恢复](QuickRecovery.md) 应该检查的沙箱化文件夹。可以指定 [系统文件夹](ShellFolders.md)。例如：
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

前两个示例设置指定，从 DefaultBox 沙箱进行 [快速恢复](QuickRecovery.md) 时，应检查 C 盘的“文档”和“下载”文件夹。

第三个示例设置指定，从 InstallBox 沙箱进行快速恢复时，应检查 D 盘的“程序文件”文件夹。

请注意，当 [快速恢复](QuickRecovery.md) 检查指定文件夹时，它还会检查该文件夹内的任何子文件夹，以及这些子文件夹内的任何子文件夹，检查的深度层级按需而定。

相关的 [沙盘控制面板](SandboxieControl.md) 设置：[沙箱设置 > 恢复 > 快速恢复](RecoverySettings.md#quick-recovery)

