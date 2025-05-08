# 启用

_Enabled_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它通常指定为 _Enabled=y_（参见[是或否设置](YesOrNoSettings.md)），表示可以在该沙盒中启动程序。例如：

```
   .
   .
   .
   [InstallBox]
   Enabled=y
   Enabled=y,Administrators
```

第一个示例是 _Enabled_ 的典型形式，是配置文件中任何沙盒部分的必需部分。它表示沙盒 _InstallBox_ 可以用于沙盒化。

第二个示例类似地定义了沙盒 _InstallBox_，同时将其使用限制为管理员用户账户组。可以指定本地 Windows 系统识别的任何用户账户或组。如果用户账户列表不适合一行，可以指定多个 _Enabled_ 行。

已限制为特定用户的沙盒对所有其他用户账户都被视为_隐藏_。这些其他用户账户将不会在 [Sandboxie Control](SandboxieControl.md) 中看到该沙盒，任何[强制进程](ForceProcess.md)或[强制文件夹](ForceFolder.md)设置都不会应用于这些用户账户。

尝试在没有关联 _Enabled=y_ 设置的沙盒中显式启动程序将失败。

相关 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 用户账户](UserAccountsSettings.md)

相关 [Sandboxie Control](SandboxieControl.md) 命令：[沙盒菜单 > 显示隐藏的沙盒](SandboxMenu.md#reveal-hidden-sandbox) 