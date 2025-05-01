# 自动恢复忽略

_AutoRecoverIgnore_ 是 [Sandboxie Ini](SandboxieIni.md) 配置文件中的一个沙箱设置。它用于指定哪些文件夹或文件类型应当被 [快速恢复](QuickRecovery.md) 的即时恢复扩展功能所忽略。例如：

```
   .
   .
   .
   [DefaultBox]
   AutoRecoverIgnore=.part
   AutoRecoverIgnore=%Desktop%
   AutoRecoverIgnore=C:\Folder
```

第一个示例排除了所有以 .part 结尾的文件，使其不会被即时恢复功能处理。这类文件通常由 Mozilla 浏览器的下载管理器创建，表示未完成的下载。当下载完成后，文件的 .part 扩展名会被删除，此时文件将符合即时恢复的条件。需要注意的是，.part 是默认设置之一。

第二和第三个示例将指定的文件夹从即时恢复范围中排除。

相关的 [Sandboxie控制](SandboxieControl.md) 设置：[沙箱设置 > 恢复 > 即时恢复](RecoverySettings.md#immediate-recovery)
