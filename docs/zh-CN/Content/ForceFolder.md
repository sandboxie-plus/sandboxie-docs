# 强制文件夹

_ForceFolder_ 是 [Sandboxie.ini](SandboxieIni.md) 中的一个沙盒设置，它允许强制文件夹内容在特定沙盒中运行。如果这些文件夹*（或这些文件夹之一的子文件夹）中的任何文件或程序在沙盒外启动，它们将自动被沙盒化到特定沙盒中。例如：

```
   .
   .
   .
   [DefaultBox]
   ForceFolder=C:\Download
   ForceFolder=E:\
```

第一个示例指定从 C:\Download 文件夹（或这些文件夹中包含的任何子文件夹）启动的文件/程序将被强制在 _DefaultBox_ 沙盒中运行。

第二个示例指定从 E 盘启动的任何文件/程序将被强制在 _DefaultBox_ 沙盒中运行。对于 CDROM 和 DVD 驱动器，这包括强制 Windows 自动启动的 _AutoRun_ 程序。

* 请注意，位于 ForceFolder 内的快捷方式，如果指向的路径不是 ForceFolder，则不会启动沙盒化应用程序。例如：如果您在 C:\ForcedFolder 中放置一个快捷方式，它指向 C:\SomeOtherPathThatIsNotForced，则该快捷方式将触发非沙盒化应用程序。

另一个考虑因素是 Modern / Store 应用程序不受支持。如果您打开特定文件类型的默认应用程序是 Windows Modern 应用程序（如 Windows 10 中的照片应用程序），则该应用程序将完全无法启动。有关更多信息，请参见[已知冲突](KnownConflicts.md#uwp--modern--microsoft-store-apps)页面。

另见：[ForceProcess](ForceProcess.md)。如果 _ForceFolder_ 和 _ForceProcess_ 都适用于正在启动的程序，则 ForceFolder 设置优先。

相关 [Sandboxie 控制](SandboxieControl.md) 设置：[沙盒设置 > 程序启动 > 强制文件夹](ProgramStartSettings.md#forced-folders) 