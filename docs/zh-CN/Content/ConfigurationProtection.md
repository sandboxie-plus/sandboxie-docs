# 配置保护

最初，任何使用 [沙箱控制](SandboxieControl.md) 或 [Sandman](PlusMigrationGuide.md) 界面的人都可以更改任何 Sandboxie 配置的内容，这些配置被存储在 [Sandboxie Ini](SandboxieIni.md) 配置文件中。此外，任何能够访问该配置文本文件的人也可以操作该配置，并将其重新加载到 Sandboxie 中。

可以启用对 [Sandboxie Ini](SandboxieIni.md) 配置文件的保护，以防止未经授权的更改。Sandboxie 提供了四种保护模式：

- 只有管理员用户账户可以进行更改（参考：[仅限管理员编辑](EditAdminOnly.md)）
- 必须输入密码才能进行更改（参考：[编辑密码](EditPassword.md)）
- 只有管理员用户账户可以使用暂停强制程序命令（参考：[强制禁用仅限管理员](ForceDisableAdminOnly.md)）
- 当主窗口隐藏时清除密码（参考：ForgetPassword）

所有保护模式可以同时启用。

保护措施适用于 [Sandboxie Ini](SandboxieIni.md) 配置文件中的 **Global Settings**、**Sandbox Settings** 和 **Template Settings** 部分。不适用于任何存储每用户偏好的 **User Settings** 部分。

要在 [沙箱控制](SandboxieControl.md) 中启用保护，请使用 [配置菜单 > 锁定配置](ConfigureMenu.md#lock-configuration) 命令。

要在 [Sandman](PlusMigrationGuide.md) 中启用保护，请使用 菜单选项 > 全局设置 > 高级配置 > Sandboxie.ini 预设 > 配置保护 命令。

* * *

为防止保护被规避，请考虑以下要点：

**配置文件的位置：** 如 [Sandboxie Ini](SandboxieIni.md) 页面所述，Sandboxie 首先会在 Windows 文件夹查找其配置文件，其次才会在 Sandboxie 安装文件夹查找。应在存放于 Windows 文件夹中的配置文件上应用保护措施。

如果只对 Sandboxie 安装文件夹中的配置文件应用保护，攻击者可能会在 Windows 文件夹中创建一个空的配置文件。这会导致 Sandboxie 下次读取配置时，实际上禁用了保护，因为 Sandboxie 会切换使用新创建且未启用保护的空配置文件。

**配置文件的访问权限：** 应将 [Sandboxie Ini](SandboxieIni.md) 配置文件的权限设置为仅允许 SYSTEM 账户拥有写入权限。其他任何用户账户仍需能够读取配置，因此应为用户组 **Authenticated Users** 或 **Everyone** 保留读取权限。
