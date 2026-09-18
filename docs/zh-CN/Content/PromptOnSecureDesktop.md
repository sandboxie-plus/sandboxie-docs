# 安全桌面上的提示

**安全桌面上的提示** 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局沙盒设置，自 v1.16.0 / 5.71.0 起可用。它控制沙盒化应用程序发出的用户帐户控制（UAC）提升提示是否出现在安全桌面上，同时不影响宿主系统行为。

**注意：** 此设置仅在启用 [使用 Sandboxie UAC](UseSandboxieUAC.md) 时生效。

用法：

```ini
   .
   .
   .
   [GlobalSettings]
   PromptOnSecureDesktop=n
```

此设置确保沙盒化应用程序的 UAC 提示不出现在安全桌面上，即使系统配置为其他方式。
