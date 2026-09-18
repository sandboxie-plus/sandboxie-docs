# 强制进程

_ForceProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定程序名称。如果这些程序中的任何一个在沙盒外启动，它们将被自动沙盒化到特定沙盒中。例如：

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

- `*` 表示任意字符序列。
- `?` 表示单个字符。

此示例指定 Internet Explorer（iexplore.exe）、Firefox（firefox.exe）、App*（Appga、App03 等）和 App?（App1、Appg、Appa 等）将被强制在沙盒 _DefaultBox_ 中运行。Outlook.exe 和 cl?cke?（clicker、clicked 等）将被强制在沙盒 _MailBox_ 中运行。

注意：_ForceProcess_ 设置只适用于以非沙盒化方式启动的程序。如果程序被专门启动到某个沙盒中，或由已在沙盒中的程序启动，则不会应用 _ForceProcess_ 设置。

另请参阅：[强制文件夹](ForceFolder.md)。如果 _ForceFolder_ 和 _ForceProcess_ 都适用于某个正在启动的程序，则强制文件夹设置优先。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 程序启动 > 强制程序](ProgramStartSettings.md#强制程序)

另请参阅：[程序设置](ProgramSettings.md#页面-1)。
