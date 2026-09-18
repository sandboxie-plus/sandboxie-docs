# 配置保护

最初，任何使用 [沙盒管理器](SandboxieControl.md)（经典版）或 [沙盒管理器](PlusMigrationGuide.md)（Plus 版）界面的人都可以更改 Sandboxie 配置的任何方面，配置存储在 [Sandboxie Ini](SandboxieIni.md) 配置文件中。此外，任何能访问配置文本文件的人都可以操作配置并将其重新加载到 Sandboxie 中。

可以激活对 [Sandboxie Ini](SandboxieIni.md) 配置文件免于未授权更改的保护。Sandboxie 提供四种保护模式：

* 只有管理员用户帐户可以做出更改（另请参阅：[仅管理员可编辑](EditAdminOnly.md)。）
* 必须输入密码才能做出更改（另请参阅：[编辑密码](EditPassword.md)。）
* 只有管理员用户帐户可以使用暂停强制程序命令（另请参阅：[仅限管理员强制禁用](ForceDisableAdminOnly.md)。）
* 主窗口隐藏时清除密码（另请参阅：忘记密码。）

所有模式可以同时处于活动状态。

保护适用于 [Sandboxie Ini](SandboxieIni.md) 配置文件的**全局设置**、**沙盒设置**和**模板设置**节。它不适用于存储每用户偏好的任何**用户设置**节。

要在 [沙盒管理器](SandboxieControl.md) 中激活保护，请使用 [配置菜单 > 锁定配置](ConfigureMenu.md#锁定配置) 命令。

要在 [沙盒管理器](PlusMigrationGuide.md)（Plus 版）中激活保护，请使用选项菜单 > 全局设置 > 高级配置 > Sandboxie.ini 预设 > 配置保护命令。

* * *

为防止绕过保护，请考虑以下几点：

**配置文件的位置：** 如 [Sandboxie Ini](SandboxieIni.md) 页面所述，Sandboxie 首先在 Windows 文件夹中查找其配置文件，然后在 Sandboxie 安装文件夹中查找。保护应应用于位于 Windows 文件夹中的配置文件。

如果保护应用于 Sandboxie 安装文件夹中的配置文件，攻击者可能会在 Windows 文件夹中创建一个空的配置文件。这将在 Sandboxie 下次读取其配置时有效地停用保护。发生这种情况是因为 Sandboxie 会转而使用新的空配置文件，而该文件未激活保护。

**对配置文件的访问：** 调整 [Sandboxie Ini](SandboxieIni.md) 配置文件的权限，只允许 SYSTEM 帐户写入。任何其他用户帐户仍必须能够读取配置，因此读取访问应授予**经过身份验证的用户**或**所有人**用户组。
