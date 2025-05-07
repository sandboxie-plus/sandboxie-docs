# 启用

_Enabled_ 是一个在 [Sandboxie Ini](SandboxieIni.md) 中的沙箱设置。它通常以 _Enabled=y_ 的形式指定（参见 [是或否设置](YesOrNoSettings.md)），用于指示该沙箱中可以启动程序。例如：

```
   .
   .
   .
   [InstallBox]
   Enabled=y
   Enabled=y,Administrators
```

第一个例子是 _Enabled_ 的常见形式，是配置文件中任何沙箱部分的必需项。它表示沙箱 _InstallBox_ 可以用于沙箱操作。

第二个例子同样定义了沙箱 _InstallBox_，但同时将其使用权限限制为 Administrators 用户帐户组。可以指定本地 Windows 系统所识别的任何用户帐户或用户组。如果用户帐户列表一行写不下，可以指定多行 _Enabled_。

被限制为特定用户的沙箱对于其他所有用户帐户来说被视为 _隐藏_。这些其他用户帐户不会在 [沙盒控制](SandboxieControl.md) 中看到该沙箱，并且任何 [Force Process](ForceProcess.md) 或 [Force Folder](ForceFolder.md) 设置对于这些用户帐户都不会生效。

如果尝试在没有相关 _Enabled=y_ 设置的沙箱中显式启动程序，则会失败。

相关 [沙盒控制](SandboxieControl.md) 设置: [沙箱设置 > 用户帐户](UserAccountsSettings.md)

相关 [沙盒控制](SandboxieControl.md) 命令: [沙箱菜单 > 显示隐藏沙箱](SandboxMenu.md#reveal-hidden-sandbox)