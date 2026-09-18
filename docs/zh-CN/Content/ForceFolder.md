# 强制文件夹

_ForceFolder_ 是 [Sandboxie.ini](SandboxieIni.md) 中的一项沙盒设置，它允许强制把文件夹内容运行在特定沙盒中。如果这些文件夹*（或其某个子文件夹）中的任何文件或程序在沙盒外启动，它们将被自动沙盒化到特定沙盒中。例如：

```
   .
   .
   .
   [DefaultBox]
   ForceFolder=C:\Download
   ForceFolder=E:\
```

第一个示例指定：从 C:\Download 文件夹（或其下包含的任何文件夹）启动的文件/程序，将被强制在沙盒 _DefaultBox_ 中运行。

第二个示例指定：从 E 盘启动的任何文件/程序，将被强制在沙盒 _DefaultBox_ 中运行。对于 CDROM 和 DVD 驱动器，这包括强制由 Windows 自动启动的 _AutoRun_ 程序。

*   请记住：位于强制文件夹内、却指向非强制文件夹路径的快捷方式，不会启动沙盒化应用程序。例如：如果你把一个快捷方式放在 C:\ForcedFolder 内，而它指向 C:\SomeOtherPathThatIsNotForced，那么该快捷方式会触发非沙盒化应用程序。

另一个注意事项：不支持新式 / Store 应用。如果你打开特定文件类型的默认应用程序是 Windows 新式应用（如 Windows 10 中的照片应用），该应用程序根本不会启动。更多信息请参阅 [已知冲突](KnownConflicts.md#microsoft-store-应用) 页面。

另请参阅：[强制进程](ForceProcess.md)。如果 _ForceFolder_ 和 _ForceProcess_ 都适用于某个正在启动的程序，则强制文件夹设置优先。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 程序启动 > 强制文件夹](ProgramStartSettings.md#强制文件夹)
