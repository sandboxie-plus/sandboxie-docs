# 用户账户设置

[Sandboxie 控制](SandboxieControl.md) > [沙箱设置](SandboxSettings.md) > 用户账户：

![](../Media/UserAccountsSettings.png)

此设置页面可将此沙箱的使用限制为特定的用户账户。“添加用户”按钮会打开一个标准的 Windows 用户账户选择对话框，可用于查找和选择特定的用户账户。也可以指定用户账户组。

已限制为特定用户使用的沙箱对所有其他用户账户而言被视为隐藏。其他用户账户将不会在 [Sandboxie 控制](SandboxieControl.md) 中看到该沙箱的列表，并且 [强制程序](ProgramStartSettings.md#forced-programs) 和 [强制文件夹](ProgramStartSettings.md#forced-folders) 设置将不适用于这些用户账户。

任何沙箱对其隐藏的用户账户，在 [Sandboxie 控制](SandboxieControl.md) 的 [沙箱菜单](SandboxMenu.md) 中会出现 [显示隐藏沙箱](SandboxMenu.md#reveal-hidden-sandbox) 命令。

相关 [Sandboxie 配置文件](SandboxieIni.md) 设置：[启用](Enabled.md)