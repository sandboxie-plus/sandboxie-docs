# 开放凭据

_OpenCredentials_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它通常指定为 _OpenCredentials=y_（参见[是或否设置](YesOrNoSettings.md)），表示 Sandboxie 不应在沙盒中隔离 Windows 凭据。例如：
```
   .
   .
   .
   [DefaultBox]
   OpenCredentials=y
```

表示在 DefaultBox 沙盒中运行的程序将更新真实的凭据存储，而不是其沙盒化实例。

Windows 凭据主要由 Windows 和 Microsoft 应用程序用于存储以下内容的用户名和密码信息：

* 网络共享
* Microsoft 账户

要管理 Windows 凭据，请启动控制面板 > 用户账户，选择一个账户，然后点击标记为_管理我的网络密码_的相关任务。

**注意：** Sandboxie 将凭据存储在沙盒化的受保护存储中。因此，如果在[沙盒设置 > 应用程序 > Web 浏览器](ApplicationsSettings.md#web-browser)中启用了_在沙盒外保存：搜索字符串和已调用命令的历史记录_设置，则无论 OpenCredentials 设置如何，凭据都不会存储在沙盒中。

~~相关的 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 应用程序 > Web 浏览器](ApplicationsSettings.md#web-browser)中的_在沙盒外保存：Hotmail 和 Messenger 的账户信息_~~（自 Sandboxie v0.8.0 / 5.50.0 版本起不再可用）

相关的 Sandboxie Plus 设置：沙盒选项 > 常规选项 > 限制 > 其他限制 > 开放系统受保护存储 