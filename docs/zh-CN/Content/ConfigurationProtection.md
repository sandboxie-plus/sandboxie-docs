# 配置保护

最初，任何使用 [Sandboxie Control](SandboxieControl.md) 或 [Sandman](PlusMigrationGuide.md) 界面的用户都可以更改存储在 [Sandboxie Ini](SandboxieIni.md) 配置文件中的 Sandboxie 配置的任何方面。此外，任何能够访问配置文本文件的人也可以操作配置并将其重新加载到 Sandboxie 中。

可以激活对 [Sandboxie Ini](SandboxieIni.md) 配置文件的保护，防止未经授权的更改。Sandboxie 提供四种保护模式：

* 只有管理员用户账户才能进行更改（另请参阅：[EditAdminOnly](EditAdminOnly.md)。）
* 必须输入密码才能进行更改（另请参阅：[EditPassword](EditPassword.md)。）
* 只有管理员用户账户才能使用暂停强制程序命令（另请参阅：[ForceDisableAdminOnly](ForceDisableAdminOnly.md)。）
* 当主窗口隐藏时清除密码（另请参阅：ForgetPassword。）

所有模式可以同时激活。

保护适用于 [Sandboxie Ini](SandboxieIni.md) 配置文件的**全局设置**、**沙盒设置**和**模板设置**部分。它不适用于任何**用户设置**部分，这些部分存储每个用户的偏好设置。

要在 [Sandboxie Control](SandboxieControl.md) 中激活保护，请使用[配置菜单 > 锁定配置](ConfigureMenu.md#lock-configuration)命令。

要在 [Sandman](PlusMigrationGuide.md) 中激活保护，请使用选项菜单 > 全局设置 > 高级配置 > Sandboxie.ini 预设 > 配置保护命令。

* * *

为防止绕过保护，请考虑以下几点：

**配置文件的位置：** 如 [Sandboxie Ini](SandboxieIni.md) 页面所述，Sandboxie 首先在 Windows 文件夹中查找其配置文件，其次在 Sandboxie 安装文件夹中查找。保护应该应用于位于 Windows 文件夹中的配置文件。

如果保护应用于 Sandboxie 安装文件夹中的配置文件，攻击者可能会在 Windows 文件夹中创建一个空的配置文件。这将在 Sandboxie 下次读取其配置时有效地停用保护。这是因为 Sandboxie 将切换到使用新的空配置文件，而该文件的保护未被激活。

**对配置文件的访问：** 调整 [Sandboxie Ini](SandboxieIni.md) 配置文件的权限，仅允许 SYSTEM 账户进行写入访问。任何其他用户账户仍然必须能够读取配置，因此应该允许用户组**已认证用户**或**所有人**进行读取访问。 