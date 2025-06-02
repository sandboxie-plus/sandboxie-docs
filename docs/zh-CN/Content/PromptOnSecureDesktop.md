# 安全桌面上的提示

**PromptOnSecureDesktop** 是 [Sandboxie Ini](SandboxieIni.md) 中自 v1.16.0 / 5.71.0 版本开始提供的全局沙盒设置。它控制来自沙盒应用程序的用户账户控制 (UAC) 提升提示是否在安全桌面上显示，同时不影响主机系统行为。

**注意：** 此设置仅在启用 [使用沙盒 UAC](UseSandboxieUAC.md) 时有效。

用法：

```ini
   .
   .
   .
   [GlobalSettings]
   PromptOnSecureDesktop=n
```

此设置确保来自沙盒应用程序的 UAC 提示不会在安全桌面上显示，即使系统配置为其他方式。


