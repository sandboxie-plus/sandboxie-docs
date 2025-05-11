# 强制进程

_ForceProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。它用于指定程序的名称。如果这些程序从任何非沙箱环境启动，则会自动在指定的沙箱中运行。例如：

```
   .
   .
   .
   [DefaultBox]
   ForceProcess=iexplore.exe
   ForceProcess=firefox.exe
   ForceProcess=App*.exe
   ForceProcess=App?.exe
   [MailBox]
   ForceProcess=outlook.exe
   ForceProcess=cl?cke?.exe
```

- `*` 代表任意多个字符
- `?` 代表一个字符

这个示例指定了 Internet Explorer（iexplore.exe）、Firefox（firefox.exe）、App* （如 Appga、App03 等），以及 App?（如 App1、Appg、Appa 等）将被强制在 _DefaultBox_ 沙箱中运行。Outlook.exe 和 cl?cke?（如 clicker、clicked 等）将被强制在 _MailBox_ 沙箱中运行。

请注意，_ForceProcess_ 设置仅对那些从未沙箱环境启动的程序生效。如果某个程序是专门在沙箱中启动，或者由已经在沙箱中运行的程序启动，那么 _ForceProcess_ 设置将不会应用。

另见：[ForceFolder](ForceFolder.md)。如果某个正在启动的程序同时匹配 _ForceFolder_ 和 _ForceProcess_ 设定，则优先应用 ForceFolder 设置。

相关 [沙盘控制](SandboxieControl.md) 设置：[沙箱设置 > 程序启动 > 强制程序](ProgramStartSettings.md#forced-programs)。

另见：[程序设置](ProgramSettings.md#page-1)