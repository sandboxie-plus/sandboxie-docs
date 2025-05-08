# 自动恢复忽略

_AutoRecoverIgnore_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置。它指定了[快速恢复](QuickRecovery.md)的即时恢复扩展应忽略的文件夹或文件类型。例如：

```
   .
   .
   .
   [DefaultBox]
   AutoRecoverIgnore=.part
   AutoRecoverIgnore=%Desktop%
   AutoRecoverIgnore=C:\Folder
```

第一个示例从即时恢复中排除了任何以 _.part_ 结尾的文件。这些文件由 Mozilla 浏览器的下载管理器创建，表示未完成的下载。当下载完成时，文件将不再具有 _.part_ 扩展名，从而使其有资格进行即时恢复。请注意，_.part_ 是默认设置。

第二个和第三个示例从即时恢复中排除了指定的文件夹。

相关的 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 恢复 > 即时恢复](RecoverySettings.md#immediate-recovery) 