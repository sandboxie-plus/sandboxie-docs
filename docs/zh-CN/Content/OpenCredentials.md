# 开放凭据

OpenCredentials 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。通常写作 `OpenCredentials=y`（参见 [Yes Or No Settings](YesOrNoSettings.md)），用于指示沙箱不应隔离 Windows 凭据。例如：
```
   .
   .
   .
   [DefaultBox]
   OpenCredentials=y
```

表示在 `DefaultBox` 沙箱中运行的程序将会更新真实的凭据库，而不是更新沙箱中的凭据库实例。

Windows 凭据主要被 Windows 及 Microsoft 应用程序用于存储以下信息的用户名和密码：

* 网络共享
* Microsoft 账户

若要管理 Windows 凭据，请依次打开控制面板 > 用户账户，选择某个账户，然后点击“相关任务”中的 _管理我的网络密码_。

**注意：** 沙盘会将凭据保存到沙箱保护存储中。因此，如果在 [沙盘设置 > 应用程序 > 网络浏览器](ApplicationsSettings.md#web-browser) 中启用了 _沙盘外保存：搜索字符串和已调用命令的历史记录_ 设置，则无论 OpenCredentials 设置如何，凭据都不会被保存在沙箱内。

~~相关 [沙盘控制](SandboxieControl.md) 设置：“沙盘外保存：Hotmail 和 Messenger 的账户信息”（自 Sandboxie v0.8.0 / 5.50.0 起不再提供）~~

相关 Sandboxie Plus 设置：沙箱选项 > 常规选项 > 限制 > 其他限制 > 打开系统保护存储