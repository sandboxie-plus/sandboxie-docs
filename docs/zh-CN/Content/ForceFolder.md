# 强制文件夹

_ForceFolder_ 是 [Sandboxie.ini](SandboxieIni.md) 中的一个沙箱设置项，用于强制文件夹内的内容在特定沙箱内运行。如果任何这些文件夹*（或其子文件夹）中的文件或程序在未处于沙箱的情况下启动，它们将自动被放入特定沙箱中运行。例如：

```
   .
   .
   .
   [DefaultBox]
   ForceFolder=C:\Download
   ForceFolder=E:\
```

第一个示例指定，从 C:\Download 文件夹（以及该文件夹下的所有子文件夹）启动的文件或程序将被强制在 _DefaultBox_ 沙箱中运行。

第二个示例指定，从 E 盘启动的任何文件或程序都将被强制在 _DefaultBox_ 沙箱中运行。对于 CDROM 和 DVD 驱动器，这也包括被 Windows 自动启动的 _AutoRun_ 程序。

* 请注意，如果位于强制文件夹（ForceFolder）中的快捷方式所指向的路径不是受强制保护的文件夹，则不会启动沙箱化的应用程序。例如：如果你在 C:\ForcedFolder 内放置一个快捷方式，但它指向 C:\SomeOtherPathThatIsNotForced，那么该快捷方式将启动一个非沙箱化的应用程序。

另一个需要注意的是，不支持现代应用/商店应用。如果你用于打开特定文件类型的默认应用是 Windows 现代应用（如 Windows 10 下的 Photos 应用），则该应用将无法启动。有关详细信息，请参见 [已知冲突](KnownConflicts.md#uwp--modern--microsoft-store-apps) 页面。

另请参阅：[强制进程](ForceProcess.md)。如果在一个程序启动时，_ForceFolder_ 和 _ForceProcess_ 条件同时适用，则优先采用 ForceFolder 设置。

相关 [沙盘控制](SandboxieControl.md) 设置：[沙箱设置 > 程序启动 > 强制文件夹](ProgramStartSettings.md#forced-folders)