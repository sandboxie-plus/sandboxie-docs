# MSI 安装程序豁免

_MsiInstallerExemptions_ 是自 v0.7.2 / 5.49.0 版本起在 [Sandboxie Ini](SandboxieIni.md) 中提供的一个沙箱设置。

```
   .
   .
   .
   [DefaultBox]
   MsiInstallerExemptions=y
```

使用 `MsiInstallerExemptions=y` 选项可允许 `MSIServer` 以沙箱化的系统令牌运行，并在需要时应用其他例外。此选项可能有助于安装 MSI 安装包。

相关 Sandboxie Plus 设置：沙箱选项 > 安全选项 > 安全强化 > 允许 MSIServer 在沙箱内使用系统令牌运行，并在必要时给予其它限制权限的豁免